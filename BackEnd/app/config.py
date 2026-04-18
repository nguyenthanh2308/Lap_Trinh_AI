from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application configuration settings"""
    app_name: str = "AI Short Story Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Model settings
    model_folder: str = "./fine_tuned_model"  # Path to fine-tuned model folder
    max_length: int = 200
    device: Optional[str] = None  # Auto-detect if None (GPU if available, else CPU)
    
    # CORS settings
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
