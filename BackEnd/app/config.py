from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration settings"""
    app_name: str = "AI Short Story Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Model settings
    model_name: str = "gpt2"  # Can be changed to fine-tuned model path
    device: str = "cpu"  # or "cuda" if GPU available
    max_length: int = 200
    
    # CORS settings
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
