"""
Git Repository Analyzer
Handles cloning and analyzing git repositories with comprehensive metrics
"""

import os
import shutil
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, TypedDict
from pathlib import Path
from collections import Counter
import logging

import git
from git import Repo, GitCommandError

from app.core.config import settings

logger = logging.getLogger(__name__)


class GitAnalysisResult(TypedDict):
    """Type definition for git analysis results"""
    analysis_id: str
    repo_name: str
    repo_url: str
    repo_path: str
    
    # Commit metrics
    total_commits: int
    first_commit_date: str
    last_commit_date: str
    days_since_last_commit: int
    
    # Contributors
    top_contributors: List[Dict[str, any]]
    total_contributors: int
    
    # Branches
    branch_names: List[str]
    total_branches: int
    default_branch: str
    
    # Recent activity
    last_10_commits: List[Dict[str, str]]
    
    # Warning signs in commits
    has_fix_commits: bool
    has_bug_commits: bool
    has_broken_commits: bool
    has_todo_commits: bool
    has_wip_commits: bool
    has_revert_commits: bool
    has_hotfix_commits: bool
    warning_commit_count: int
    warning_commit_percentage: float
    
    # File analysis
    file_extensions: Dict[str, int]
    total_files: int
    total_directories: int
    
    # Dependency files detected
    has_requirements_txt: bool
    has_package_json: bool
    has_pom_xml: bool
    has_go_mod: bool
    has_gemfile: bool
    has_cargo_toml: bool
    dependency_files: List[str]
    
    # Documentation
    has_readme: bool
    readme_files: List[str]
    
    # Testing
    has_tests: bool
    test_files: List[str]
    test_file_count: int


class GitAnalyzer:
    """
    Analyzes git repositories for archaeological insights.
    Pure git analysis without AI - extracts raw metrics and patterns.
    """
    
    # Keywords to detect problematic commits
    WARNING_KEYWORDS = {
        'fix': 'has_fix_commits',
        'bug': 'has_bug_commits',
        'broken': 'has_broken_commits',
        'todo': 'has_todo_commits',
        'wip': 'has_wip_commits',
        'revert': 'has_revert_commits',
        'hotfix': 'has_hotfix_commits',
    }
    
    # Dependency file patterns
    DEPENDENCY_FILES = {
        'requirements.txt': 'has_requirements_txt',
        'package.json': 'has_package_json',
        'pom.xml': 'has_pom_xml',
        'go.mod': 'has_go_mod',
        'Gemfile': 'has_gemfile',
        'Cargo.toml': 'has_cargo_toml',
    }
    
    # README patterns (case-insensitive)
    README_PATTERNS = ['readme.md', 'readme.txt', 'readme.rst', 'readme']
    
    # Test file patterns
    TEST_PATTERNS = ['test_', '_test.', 'spec.', '.spec.', '_spec.', 'test/', '/tests/', '/test/']
    
    def __init__(self):
        """Initialize the analyzer and create temp directory"""
        self.temp_dir = Path(settings.TEMP_REPO_DIR)
        self.temp_dir.mkdir(exist_ok=True)
        logger.info(f"GitAnalyzer initialized with temp dir: {self.temp_dir}")
    
    async def clone_and_analyze(self, repo_url: str) -> GitAnalysisResult:
        """
        Clone a repository and perform comprehensive analysis.
        
        Args:
            repo_url: GitHub repository URL (e.g., https://github.com/user/repo)
            
        Returns:
            GitAnalysisResult dictionary with all analysis data
            
        Raises:
            GitCommandError: If cloning fails
            ValueError: If repo_url is invalid
            Exception: For other analysis errors
        """
        # Validate URL
        if not repo_url or not isinstance(repo_url, str):
            raise ValueError("Invalid repository URL")
        
        # Generate unique analysis ID
        analysis_id = str(uuid.uuid4())
        repo_path = self.temp_dir / analysis_id
        
        logger.info(f"Starting analysis for {repo_url} with ID {analysis_id}")
        
        try:
            # Clone repository
            logger.info(f"Cloning repository to {repo_path}")
            repo = Repo.clone_from(repo_url, repo_path, depth=None)  # Full clone for complete history
            logger.info("Repository cloned successfully")
            
            # Extract repository name from URL
            repo_name = self._extract_repo_name(repo_url)
            
            # Perform all analyses
            result: GitAnalysisResult = {
                'analysis_id': analysis_id,
                'repo_name': repo_name,
                'repo_url': repo_url,
                'repo_path': str(repo_path),
                
                # Analyze commits
                **self._analyze_commits(repo),
                
                # Analyze contributors
                **self._analyze_contributors(repo),
                
                # Analyze branches
                **self._analyze_branches(repo),
                
                # Analyze commit messages for warnings
                **self._analyze_commit_warnings(repo),
                
                # Analyze file structure
                **self._analyze_files(repo_path),
                
                # Detect dependency files
                **self._detect_dependency_files(repo_path),
                
                # Check for documentation
                **self._check_documentation(repo_path),
                
                # Check for tests
                **self._check_tests(repo_path),
            }
            
            logger.info(f"Analysis complete for {repo_name}")
            return result
            
        except GitCommandError as e:
            logger.error(f"Git command failed: {str(e)}")
            # Cleanup on failure
            if repo_path.exists():
                shutil.rmtree(repo_path, ignore_errors=True)
            raise Exception(f"Failed to clone repository: {str(e)}")
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            # Cleanup on failure
            if repo_path.exists():
                shutil.rmtree(repo_path, ignore_errors=True)
            raise
    
    def _extract_repo_name(self, repo_url: str) -> str:
        """
        Extract repository name from URL.
        Handles: https://github.com/user/repo, https://github.com/user/repo.git
        """
        name = repo_url.rstrip('/').split('/')[-1]
        return name.replace('.git', '')
    
    def _analyze_commits(self, repo: Repo) -> Dict:
        """
        Analyze commit history to extract metrics.
        
        Returns:
            Dict with total_commits, first_commit_date, last_commit_date, 
            days_since_last_commit, last_10_commits
        """
        try:
            # Get all commits (this might be slow for huge repos, but we need accurate count)
            all_commits = list(repo.iter_commits('HEAD'))
            
            if not all_commits:
                logger.warning("No commits found in repository")
                return {
                    'total_commits': 0,
                    'first_commit_date': None,
                    'last_commit_date': None,
                    'days_since_last_commit': 0,
                    'last_10_commits': [],
                }
            
            # Get first and last commits
            last_commit = all_commits[0]  # Most recent
            first_commit = all_commits[-1]  # Oldest
            
            # Calculate days since last commit
            now = datetime.now(timezone.utc)
            last_commit_date = last_commit.committed_datetime
            days_since = (now - last_commit_date).days
            
            # Get last 10 commits with details
            last_10 = []
            for commit in all_commits[:10]:
                last_10.append({
                    'hash': commit.hexsha[:7],
                    'message': commit.message.strip(),
                    'author': commit.author.name,
                    'date': commit.committed_datetime.isoformat(),
                })
            
            return {
                'total_commits': len(all_commits),
                'first_commit_date': first_commit.committed_datetime.isoformat(),
                'last_commit_date': last_commit.committed_datetime.isoformat(),
                'days_since_last_commit': days_since,
                'last_10_commits': last_10,
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze commits: {str(e)}")
            return {
                'total_commits': 0,
                'first_commit_date': None,
                'last_commit_date': None,
                'days_since_last_commit': 0,
                'last_10_commits': [],
            }
    
    def _analyze_contributors(self, repo: Repo) -> Dict:
        """
        Analyze contributors and their commit counts.
        
        Returns:
            Dict with top_contributors (top 3) and total_contributors
        """
        try:
            commits = list(repo.iter_commits('HEAD'))
            
            if not commits:
                return {
                    'top_contributors': [],
                    'total_contributors': 0,
                }
            
            # Count commits per author
            author_commits = Counter()
            author_details = {}
            
            for commit in commits:
                author_name = commit.author.name
                author_email = commit.author.email
                
                author_commits[author_name] += 1
                
                # Store author details (will be overwritten, but that's fine)
                if author_name not in author_details:
                    author_details[author_name] = {
                        'name': author_name,
                        'email': author_email,
                        'commits': 0,
                    }
            
            # Update commit counts
            for author, count in author_commits.items():
                author_details[author]['commits'] = count
            
            # Get top 3 contributors
            top_3 = sorted(
                author_details.values(),
                key=lambda x: x['commits'],
                reverse=True
            )[:3]
            
            return {
                'top_contributors': top_3,
                'total_contributors': len(author_details),
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze contributors: {str(e)}")
            return {
                'top_contributors': [],
                'total_contributors': 0,
            }
    
    def _analyze_branches(self, repo: Repo) -> Dict:
        """
        Analyze branch structure.
        
        Returns:
            Dict with branch_names, total_branches, default_branch
        """
        try:
            # Get all branches
            branches = [branch.name for branch in repo.branches]
            
            # Get default/active branch
            try:
                default_branch = repo.active_branch.name
            except TypeError:
                # Detached HEAD state
                default_branch = "detached"
            
            return {
                'branch_names': branches,
                'total_branches': len(branches),
                'default_branch': default_branch,
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze branches: {str(e)}")
            return {
                'branch_names': [],
                'total_branches': 0,
                'default_branch': 'unknown',
            }
    
    def _analyze_commit_warnings(self, repo: Repo) -> Dict:
        """
        Analyze commit messages for warning keywords.
        Detects: fix, bug, broken, TODO, WIP, revert, hotfix
        
        Returns:
            Dict with boolean flags for each keyword and warning statistics
        """
        try:
            commits = list(repo.iter_commits('HEAD'))
            
            if not commits:
                # Return all False if no commits
                result = {key: False for key in self.WARNING_KEYWORDS.values()}
                result.update({
                    'warning_commit_count': 0,
                    'warning_commit_percentage': 0.0,
                })
                return result
            
            # Initialize counters
            warning_flags = {key: False for key in self.WARNING_KEYWORDS.values()}
            warning_commit_count = 0
            commits_with_warnings = set()
            
            # Scan all commit messages
            for commit in commits:
                # Get message and convert to lowercase for case-insensitive matching
                message = commit.message.lower()
                commit_has_warning = False
                
                # Check each warning keyword
                for keyword, flag_name in self.WARNING_KEYWORDS.items():
                    if keyword in message:
                        warning_flags[flag_name] = True
                        commit_has_warning = True
                
                # Track unique commits with warnings
                if commit_has_warning:
                    commits_with_warnings.add(commit.hexsha)
            
            warning_commit_count = len(commits_with_warnings)
            warning_percentage = (warning_commit_count / len(commits)) * 100 if commits else 0.0
            
            # Combine results
            result = warning_flags.copy()
            result.update({
                'warning_commit_count': warning_commit_count,
                'warning_commit_percentage': round(warning_percentage, 2),
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to analyze commit warnings: {str(e)}")
            result = {key: False for key in self.WARNING_KEYWORDS.values()}
            result.update({
                'warning_commit_count': 0,
                'warning_commit_percentage': 0.0,
            })
            return result
    
    def _analyze_files(self, repo_path: Path) -> Dict:
        """
        Analyze file structure and extensions.
        
        Returns:
            Dict with file_extensions, total_files, total_directories
        """
        try:
            file_extensions = Counter()
            total_files = 0
            total_directories = 0
            
            # Walk through directory tree
            for root, dirs, files in os.walk(repo_path):
                # Skip .git directory
                if '.git' in Path(root).parts:
                    continue
                
                total_directories += len(dirs)
                total_files += len(files)
                
                # Count file extensions
                for file in files:
                    ext = Path(file).suffix.lower()
                    if ext:
                        file_extensions[ext] += 1
                    else:
                        file_extensions['no_extension'] += 1
            
            return {
                'file_extensions': dict(file_extensions),
                'total_files': total_files,
                'total_directories': total_directories,
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze files: {str(e)}")
            return {
                'file_extensions': {},
                'total_files': 0,
                'total_directories': 0,
            }
    
    def _detect_dependency_files(self, repo_path: Path) -> Dict:
        """
        Detect common dependency management files.
        Checks for: requirements.txt, package.json, pom.xml, go.mod, Gemfile, Cargo.toml
        
        Returns:
            Dict with boolean flags for each file type and list of found files
        """
        try:
            result = {key: False for key in self.DEPENDENCY_FILES.values()}
            found_files = []
            
            # Check for each dependency file
            for filename, flag_name in self.DEPENDENCY_FILES.items():
                file_path = repo_path / filename
                if file_path.exists():
                    result[flag_name] = True
                    found_files.append(filename)
                    logger.debug(f"Found dependency file: {filename}")
            
            result['dependency_files'] = found_files
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to detect dependency files: {str(e)}")
            result = {key: False for key in self.DEPENDENCY_FILES.values()}
            result['dependency_files'] = []
            return result
    
    def _check_documentation(self, repo_path: Path) -> Dict:
        """
        Check for README files (case-insensitive).
        
        Returns:
            Dict with has_readme flag and list of readme files found
        """
        try:
            readme_files = []
            
            # Check root directory for README files
            for item in repo_path.iterdir():
                if item.is_file():
                    filename_lower = item.name.lower()
                    # Check if filename matches any README pattern
                    if any(pattern in filename_lower for pattern in self.README_PATTERNS):
                        readme_files.append(item.name)
                        logger.debug(f"Found README: {item.name}")
            
            return {
                'has_readme': len(readme_files) > 0,
                'readme_files': readme_files,
            }
            
        except Exception as e:
            logger.error(f"Failed to check documentation: {str(e)}")
            return {
                'has_readme': False,
                'readme_files': [],
            }
    
    def _check_tests(self, repo_path: Path) -> Dict:
        """
        Check for test files.
        Looks for patterns: test_, _test, spec, /test/, /tests/
        
        Returns:
            Dict with has_tests flag, list of test files, and count
        """
        try:
            test_files = []
            
            # Walk through all files
            for root, dirs, files in os.walk(repo_path):
                # Skip .git directory
                if '.git' in Path(root).parts:
                    continue
                
                # Get relative path for better readability
                rel_root = Path(root).relative_to(repo_path)
                rel_root_str = str(rel_root).lower()
                
                # Check if we're in a test directory
                in_test_dir = any(pattern in rel_root_str for pattern in ['/test/', '/tests/', 'test/'])
                
                for file in files:
                    filename_lower = file.lower()
                    
                    # Check if filename matches test patterns
                    is_test_file = (
                        filename_lower.startswith('test_') or
                        '_test.' in filename_lower or
                        filename_lower.startswith('spec.') or
                        '.spec.' in filename_lower or
                        '_spec.' in filename_lower or
                        in_test_dir
                    )
                    
                    if is_test_file:
                        # Store relative path
                        test_file_path = str(rel_root / file)
                        test_files.append(test_file_path)
            
            return {
                'has_tests': len(test_files) > 0,
                'test_files': test_files[:20],  # Limit to first 20 for brevity
                'test_file_count': len(test_files),
            }
            
        except Exception as e:
            logger.error(f"Failed to check tests: {str(e)}")
            return {
                'has_tests': False,
                'test_files': [],
                'test_file_count': 0,
            }
    
    def cleanup(self, analysis_id: str) -> bool:
        """
        Clean up temporary repository files after analysis.
        
        Args:
            analysis_id: The unique analysis ID
            
        Returns:
            True if cleanup successful, False otherwise
        """
        try:
            repo_path = self.temp_dir / analysis_id
            
            if not repo_path.exists():
                logger.warning(f"Repository path does not exist: {repo_path}")
                return False
            
            # Remove directory and all contents
            shutil.rmtree(repo_path, ignore_errors=False)
            logger.info(f"Successfully cleaned up repository: {analysis_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cleanup repository {analysis_id}: {str(e)}")
            return False
    
    def cleanup_all(self) -> int:
        """
        Clean up all temporary repositories.
        Useful for maintenance or error recovery.
        
        Returns:
            Number of repositories cleaned up
        """
        try:
            if not self.temp_dir.exists():
                logger.info("Temp directory does not exist, nothing to clean")
                return 0
            
            count = 0
            for item in self.temp_dir.iterdir():
                if item.is_dir():
                    try:
                        shutil.rmtree(item, ignore_errors=False)
                        count += 1
                        logger.debug(f"Cleaned up: {item.name}")
                    except Exception as e:
                        logger.error(f"Failed to cleanup {item.name}: {str(e)}")
            
            logger.info(f"Cleaned up {count} repositories")
            return count
            
        except Exception as e:
            logger.error(f"Failed to cleanup all repositories: {str(e)}")
            return 0

# Made with Bob
