"""
Mock WatsonX Service for testing without IBM Cloud credentials
Use this when you don't have access to IBM watsonx.ai API
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)


class MockWatsonXService:
    """
    Mock service that mimics WatsonXService behavior without making API calls.
    Perfect for development, testing, or when you don't have IBM credentials.
    """
    
    def __init__(self):
        """Initialize mock service"""
        pass
    
    async def analyze_architecture(self, git_data: Dict) -> Dict:
        """
        Generate mock architecture analysis based on git data.
        """
        repo_name = git_data.get('repo_name', 'Unknown')
        total_files = git_data.get('total_files', 0)
        dep_files = git_data.get('dependency_files', [])
        has_tests = git_data.get('has_tests', False)
        has_readme = git_data.get('has_readme', False)
        
        # Build tech stack description
        tech_desc = "multiple technologies" if len(dep_files) > 1 else "a single technology"
        if dep_files:
            tech_list = ', '.join(dep_files)
            tech_desc = f"technologies including {tech_list}"
        
        # Generate mock analysis
        analysis = f"""**Main Purpose**: Based on the repository structure, {repo_name} appears to be a software project with {total_files} files using {tech_desc}.

**Architecture Pattern**: The project follows a standard file organization pattern. {'Tests are present, indicating good development practices.' if has_tests else 'No test files detected.'} {'Documentation exists via README.' if has_readme else 'Limited documentation found.'}

**Key Components**: The codebase is organized into {git_data.get('total_directories', 0)} directories, suggesting a modular structure with separated concerns.

**Data Flow**: Based on the file structure, data likely flows through standard application layers with clear separation of concerns.

**External Dependencies**: The project uses {len(dep_files)} dependency management file(s), indicating integration with external libraries and frameworks."""
        
        return {
            "analysis": analysis,
            "file_count": total_files,
            "has_tests": has_tests,
            "has_readme": has_readme,
            "dependency_files": dep_files,
        }
    
    async def analyze_cause_of_death(self, git_data: Dict) -> Dict:
        """
        Generate mock cause of death analysis based on git data.
        """
        repo_name = git_data.get('repo_name', 'Unknown')
        days = git_data.get('days_since_last_commit', 0)
        total_commits = git_data.get('total_commits', 0)
        warning_pct = git_data.get('warning_commit_percentage', 0)
        
        # Determine severity
        if days < 90:
            severity = "low"
            status = "recently dormant"
        elif days < 365:
            severity = "medium"
            status = "moderately abandoned"
        elif days < 1095:
            severity = "high"
            status = "long abandoned"
        else:
            severity = "critical"
            status = "ancient ruins"
        
        # Generate mock analysis
        analysis = f"""**Primary Cause**: The archaeological evidence suggests {repo_name} fell silent {days} days ago, making it {status}. With {total_commits} commits in its history, this repository once showed signs of active development.

**Warning Signs**: Analysis of commit patterns reveals that {warning_pct}% of commits contained warning keywords (fix, bug, TODO, WIP, etc.), indicating potential technical challenges during development.

**Timeline of Decline**: The repository's {total_commits} commits tell a story of development that eventually ceased. The final commits occurred {days} days ago, marking the point where active development stopped.

**Severity Assessment**: Based on the time elapsed and commit patterns, this abandonment is classified as **{severity.upper()}** severity. The repository has been silent for {days} days, placing it in the "{status}" category.

**Recovery Prognosis**: {'Revival is feasible with moderate effort.' if days < 365 else 'Revival will require significant effort due to the extended abandonment period.' if days < 1095 else 'Revival presents substantial challenges due to the ancient nature of this codebase.'}"""
        
        return {
            "analysis": analysis,
            "days_since_last_commit": days,
            "warning_commit_percentage": warning_pct,
            "severity": severity,
            "total_commits": total_commits,
        }
    
    async def identify_salvageable_components(self, git_data: Dict) -> Dict:
        """
        Generate mock salvageable components analysis based on git data.
        """
        has_tests = git_data.get('has_tests', False)
        has_readme = git_data.get('has_readme', False)
        test_count = git_data.get('test_file_count', 0)
        total_commits = git_data.get('total_commits', 0)
        days = git_data.get('days_since_last_commit', 0)
        
        # Calculate salvage percentage
        salvage_pct = 30
        if has_tests:
            salvage_pct += 20
        if has_readme:
            salvage_pct += 10
        if total_commits > 100:
            salvage_pct += 15
        if days < 365:
            salvage_pct += 15
        salvage_pct = min(salvage_pct, 85)
        
        # Generate mock analysis
        analysis = f"""**High-Value Components**: {'The presence of ' + str(test_count) + ' test files indicates well-tested code that is likely reliable and reusable.' if has_tests else 'Without test files, code quality assessment is challenging, but core functionality may still be salvageable.'}

**Utility Functions**: Based on the file structure, there are likely utility functions and helper modules that could be extracted and reused in modern projects.

**Configuration Patterns**: {'Documentation exists that could provide valuable insights into configuration and setup patterns.' if has_readme else 'Limited documentation may make configuration understanding more challenging.'}

**Documentation Value**: {'README and documentation files are present, providing valuable context for understanding the codebase.' if has_readme else 'Documentation is minimal, which may complicate salvage efforts.'}

**Test Suite**: {'With ' + str(test_count) + ' test files, the test suite provides valuable insights into expected behavior and can guide refactoring efforts.' if has_tests else 'No test suite detected, which increases the risk of salvaging components without understanding their full behavior.'}

**Modern Compatibility**: Based on the {days} days since last activity, dependencies will likely need updating to work with modern toolchains and frameworks.

**Overall Assessment**: Approximately **{salvage_pct}%** of this codebase appears salvageable for reuse in modern projects, with appropriate updates and refactoring."""
        
        return {
            "analysis": analysis,
            "estimated_salvage_percentage": salvage_pct,
            "has_tests": has_tests,
            "has_readme": has_readme,
            "test_file_count": test_count,
        }
    
    async def generate_revival_plan(
        self,
        git_data: Dict,
        architecture: Dict,
        cause_of_death: Dict,
        salvageable: Dict
    ) -> Dict:
        """
        Generate mock revival plan based on all analysis data.
        """
        days = git_data.get('days_since_last_commit', 0)
        total_files = git_data.get('total_files', 0)
        severity = cause_of_death.get('severity', 'medium')
        salvage_pct = salvageable.get('estimated_salvage_percentage', 50)
        
        # Calculate estimates
        base_days = 10
        if total_files > 100:
            base_days += 15
        if severity == 'critical':
            base_days += 20
        elif severity == 'high':
            base_days += 10
        if salvage_pct < 40:
            base_days += 15
        
        # Effort estimate
        if base_days < 20:
            effort = "small (10-20 days)"
        elif base_days < 40:
            effort = "medium (20-40 days)"
        elif base_days < 60:
            effort = "large (40-60 days)"
        else:
            effort = "very large (60+ days)"
        
        # Risk level
        risk_score = 0
        if days > 1095:
            risk_score += 2
        if severity == 'critical':
            risk_score += 2
        if not git_data.get('has_tests'):
            risk_score += 1
        if salvage_pct < 40:
            risk_score += 1
        
        risk = "high" if risk_score >= 4 else "medium" if risk_score >= 2 else "low"
        
        # Team size
        team_size = 3 if total_files > 200 else 2 if total_files > 100 else 1
        
        # Timeline
        timeline_weeks = (base_days // 5) + 1
        
        # Generate mock plan
        analysis = f"""**Effort Estimation**: Revival of this project will require approximately **{base_days} developer-days** of effort, classified as a **{effort}** project.

**Priority Tasks**:
1. **Dependency Audit** (Days 1-3): Update all dependencies to current versions, resolve conflicts
2. **Environment Setup** (Days 3-5): Establish modern development environment and toolchain
3. **Core Functionality Restoration** (Days 5-{base_days//2}): Fix breaking changes, restore basic functionality
4. **Testing & Validation** (Days {base_days//2}-{base_days-5}): {'Expand existing test suite' if git_data.get('has_tests') else 'Create comprehensive test suite'}
5. **Documentation Update** (Days {base_days-5}-{base_days}): Update README, add setup instructions, document changes

**Dependency Updates**: All dependencies will need updating due to {days} days of abandonment. Expect breaking changes in major dependencies.

**Main Risks**:
1. **Dependency Hell**: Outdated dependencies may have breaking changes
2. **Lost Knowledge**: Original developers' context is unavailable
3. **Hidden Dependencies**: Undocumented system requirements may exist

**Team Requirements**:
- **Team Size**: {team_size} developer{'s' if team_size > 1 else ''}
- **Skills Needed**: Experience with the detected tech stack, dependency management, refactoring
- **Time Commitment**: {timeline_weeks} weeks at full-time capacity

**Timeline**: Realistic timeline is **{timeline_weeks} weeks** with a team of {team_size}, assuming full-time dedication.

**Success Metrics**:
1. All dependencies updated to current versions
2. Application starts without errors
3. Core functionality operational
4. {'Test suite passing' if git_data.get('has_tests') else 'Test coverage > 70%'}
5. Documentation complete and accurate

**Risk Level**: **{risk.upper()}** - {'Proceed with caution and adequate resources.' if risk == 'high' else 'Manageable with proper planning.' if risk == 'medium' else 'Low risk, good candidate for revival.'}"""
        
        return {
            "analysis": analysis,
            "effort_estimate": effort,
            "effort_days": base_days,
            "risk_level": risk,
            "recommended_team_size": team_size,
            "estimated_timeline_weeks": timeline_weeks,
        }

# Made with Bob
