"""
Application configuration using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # IBM Bob API Key
    BOB_API_KEY: Optional[str] = None
    
    # IBM Speech-to-Text (Optional)
    SPEECH_TO_TEXT_API_KEY: Optional[str] = None
    SPEECH_TO_TEXT_URL: Optional[str] = None
    
    # Application Settings
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = True
    
    # Temporary directory for cloned repositories
    TEMP_REPO_DIR: str = "temp_repos"
    
    # Report output directory
    REPORT_OUTPUT_DIR: str = "reports"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Made with Bob
