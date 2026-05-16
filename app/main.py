"""
Stack Archaeologist - Main FastAPI Application
An AI-powered tool for analyzing abandoned GitHub repositories
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, validator
from typing import List
from pathlib import Path
import logging
import re

from app.core.config import settings
from app.services.git_analyzer import GitAnalyzer
from app.services.mock_watsonx_service import MockWatsonXService
from app.services.report_generator import ReportGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Stack Archaeologist",
    description="AI-powered archaeological analysis of abandoned GitHub repositories",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class AnalyzeRequest(BaseModel):
    """Request model for repository analysis"""
    repo_url: str
    
    @validator('repo_url')
    def validate_github_url(cls, v):
        """Validate that the URL is a valid GitHub repository URL"""
        if not v:
            raise ValueError('Repository URL is required')
        
        # Check if it's a valid GitHub URL
        github_pattern = r'^https?://github\.com/[\w\-\.]+/[\w\-\.]+/?$'
        if not re.match(github_pattern, v.rstrip('/')):
            raise ValueError('Must be a valid GitHub repository URL (e.g., https://github.com/user/repo)')
        
        return v.rstrip('/')


class AnalysisResponse(BaseModel):
    """Response model for analysis results"""
    report_id: str
    repo_name: str
    days_abandoned: int
    total_commits: int
    severity: str
    tech_stack: List[str]
    report_url: str
    report_filename: str
    summary: str


# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main landing page"""
    landing_page_path = Path(__file__).parent / "templates" / "landing_page.html"
    with open(landing_page_path, 'r', encoding='utf-8') as f:
        return f.read()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "services": {
            "git_analyzer": "ready",
            "watsonx": "ready",
            "report_generator": "ready"
        }
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_repository(request: AnalyzeRequest):
    """
    Analyze a GitHub repository and generate archaeological report.
    
    Steps:
    1. Validate GitHub URL
    2. Clone and analyze repository with git_analyzer
    3. Generate AI analysis with watsonx_service
    4. Create HTML report with report_generator
    5. Cleanup cloned repository
    6. Return summary response
    """
    analysis_id = None
    
    try:
        logger.info(f"Starting analysis for repository: {request.repo_url}")
        
        # Initialize services
        git_analyzer = GitAnalyzer()
        watsonx_service = MockWatsonXService()
        report_generator = ReportGenerator()
        
        # Step 1: Clone and analyze git repository
        logger.info("Step 1/5: Cloning and analyzing repository...")
        git_data = await git_analyzer.clone_and_analyze(request.repo_url)
        analysis_id = git_data['analysis_id']
        
        # Step 2: Analyze architecture with AI
        logger.info("Step 2/5: Analyzing architecture with AI...")
        architecture = await watsonx_service.analyze_architecture(git_data)  # type: ignore
        
        # Step 3: Analyze cause of death
        logger.info("Step 3/5: Analyzing cause of death...")
        cause_of_death = await watsonx_service.analyze_cause_of_death(git_data)  # type: ignore
        
        # Step 4: Identify salvageable components
        logger.info("Step 4/5: Identifying salvageable components...")
        salvageable = await watsonx_service.identify_salvageable_components(git_data)  # type: ignore
        
        # Step 5: Generate revival plan
        logger.info("Step 5/5: Generating revival plan...")
        revival_plan = await watsonx_service.generate_revival_plan(
            git_data, architecture, cause_of_death, salvageable  # type: ignore
        )
        
        # Step 6: Generate HTML report
        logger.info("Generating HTML report...")
        report_filename = await report_generator.generate_report(
            repo_name=git_data['repo_name'],
            git_data=git_data,  # type: ignore
            architecture=architecture,
            cause_of_death=cause_of_death,
            salvageable=salvageable,
            revival_plan=revival_plan
        )
        
        # Step 7: Cleanup cloned repository
        logger.info("Cleaning up cloned repository...")
        git_analyzer.cleanup(analysis_id)
        
        # Extract summary (first sentence from architecture analysis)
        summary_text = architecture.get('analysis', 'Analysis complete.')
        summary = summary_text.split('.')[0] + '.' if '.' in summary_text else summary_text[:150]
        
        # Build tech stack list from file extensions and dependency files
        tech_stack = []
        
        # First, try to get from dependency files
        dep_files = git_data.get('dependency_files', [])
        tech_map = {
            'package.json': 'Node.js',
            'requirements.txt': 'Python',
            'pom.xml': 'Java',
            'go.mod': 'Go',
            'Gemfile': 'Ruby',
            'Cargo.toml': 'Rust',
            'Cargo.lock': 'Rust',
            'composer.json': 'PHP',
            'build.gradle': 'Java',
        }
        for dep_file in dep_files:
            if dep_file in tech_map:
                tech = tech_map[dep_file]
                if tech not in tech_stack:
                    tech_stack.append(tech)
        
        # If no dependency files, infer from file extensions
        if not tech_stack:
            file_exts = git_data.get('file_extensions', {})
            ext_map = {
                '.py': 'Python',
                '.js': 'JavaScript',
                '.ts': 'TypeScript',
                '.java': 'Java',
                '.go': 'Go',
                '.rb': 'Ruby',
                '.php': 'PHP',
                '.rs': 'Rust',
                '.cpp': 'C++',
                '.c': 'C',
                '.cs': 'C#',
                '.swift': 'Swift',
                '.kt': 'Kotlin',
            }
            for ext, count in sorted(file_exts.items(), key=lambda x: x[1], reverse=True)[:3]:
                if ext in ext_map:
                    tech = ext_map[ext]
                    if tech not in tech_stack:
                        tech_stack.append(tech)
        
        logger.info(f"Analysis complete for {git_data['repo_name']}")
        
        # Return response
        return AnalysisResponse(
            report_id=report_filename.replace('.html', ''),
            repo_name=git_data['repo_name'],
            days_abandoned=git_data['days_since_last_commit'],
            total_commits=git_data['total_commits'],
            severity=cause_of_death.get('severity', 'medium'),
            tech_stack=tech_stack,
            report_url=f"/api/report/{report_filename}",
            report_filename=report_filename,
            summary=summary
        )
        
    except ValueError as e:
        # Validation error
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        
        # Attempt cleanup if we have an analysis_id
        if analysis_id:
            try:
                git_analyzer = GitAnalyzer()
                git_analyzer.cleanup(analysis_id)
            except Exception as cleanup_error:
                logger.error(f"Cleanup failed: {str(cleanup_error)}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/api/report/{report_filename}", response_class=HTMLResponse)
async def get_report(report_filename: str):
    """
    Retrieve generated HTML report by filename.
    
    Args:
        report_filename: The report filename (e.g., repo-name-20260515-143022.html)
    
    Returns:
        HTML content of the report
    """
    try:
        # Ensure filename ends with .html
        if not report_filename.endswith('.html'):
            report_filename += '.html'
        
        # Construct file path
        report_path = Path(settings.REPORT_OUTPUT_DIR) / report_filename
        
        # Check if file exists
        if not report_path.exists():
            logger.warning(f"Report not found: {report_filename}")
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Read and return HTML content
        with open(report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        logger.info(f"Serving report: {report_filename}")
        return HTMLResponse(content=html_content)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve report: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )

# Made with Bob