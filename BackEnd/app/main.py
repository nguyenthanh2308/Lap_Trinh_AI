"""
FastAPI application for AI-Powered Short Story Generator.

This module sets up the FastAPI application with:
- Model loading on startup using lifespan context manager
- CORS middleware for frontend communication
- RESTful API routes for story generation
- Proper error handling and logging
"""

from contextlib import asynccontextmanager
from typing import Dict, Any
import logging

import torch
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.model_loader import ModelLoader
from app.api.routes import story

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """
    Manage application startup and shutdown lifecycle.
    
    This context manager handles:
    - Loading AI model and tokenizer at startup
    - Storing them in app.state for route access
    - Cleaning up GPU memory on shutdown
    
    Modern approach using FastAPI 0.93+ lifespan parameter.
    
    Args:
        app: FastAPI application instance
    
    Yields:
        None: Application runs between yield statements
    """
    # ========== STARTUP ==========
    logger.info("🚀 Application starting up...")
    try:
        # Load model from local folder
        logger.info(f"Loading fine-tuned model from: {settings.model_folder}")
        tokenizer, model, device = ModelLoader.load_model(
            model_folder=settings.model_folder,
            device=settings.device  # Auto-detect if None
        )
        
        # Store in app.state for access by routes
        app.state.tokenizer = tokenizer
        app.state.model = model
        app.state.device = device
        
        logger.info(f"✅ Model loaded successfully on device: {device}")
        logger.info("✅ Application is ready to accept requests!")
    
    except Exception as e:
        logger.error(f"❌ Failed to load model during startup: {str(e)}")
        logger.error("Application will start but inference will fail.")
        # Don't raise - let app start anyway so we can see the error
        app.state.tokenizer = None
        app.state.model = None
        app.state.device = None
    
    yield
    
    # ========== SHUTDOWN ==========
    logger.info("🛑 Application shutting down...")
    logger.info("Cleaning up resources...")
    
    # Clean up GPU memory if using CUDA
    try:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("GPU memory cleaned up")
    except Exception as e:
        logger.warning(f"Could not clean GPU memory: {str(e)}")
    
    logger.info("✅ Shutdown complete")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Configures:
    - Lifespan context manager for startup/shutdown
    - CORS middleware for frontend communication
    - API routers and endpoints
    - Health check and info endpoints
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "An AI-powered Vietnamese short story generator using fine-tuned "
            "transformer models. Accepts character details and generates creative stories."
        ),
        debug=settings.debug,
        lifespan=lifespan  # Use lifespan context manager
    )
    
    # Add CORS middleware for frontend communication
    # Allows requests from React development server and other specified origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,  # ["http://localhost:3000", "http://localhost:5173"]
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(story.router)
    
    # Root endpoint - general info about the API
    @app.get(
        "/",
        tags=["info"],
        response_description="API information and status"
    )
    async def root() -> Dict[str, Any]:
        """
        Get API information and current status.
        
        Returns:
            Dictionary with API details, version, and model status
        """
        return {
            "message": "Welcome to AI Short Story Generator API",
            "version": settings.app_version,
            "docs": "/docs",
            "redoc": "/redoc",
            "model_loaded": app.state.model is not None,
            "device": getattr(app.state, "device", "unknown"),
            "endpoints": {
                "health": "/health",
                "generate": "/api/v1/generate",
                "api_docs": "/docs"
            }
        }
    
    # Health check endpoint - simple status verification
    @app.get(
        "/health",
        tags=["health"],
        response_description="Server health status",
        status_code=200
    )
    async def health_check() -> Dict[str, str]:
        """
        Simple health check endpoint.
        
        Returns {"status": "ok"} if server is running.
        Useful for frontend to verify API availability before making requests.
        
        Returns:
            Dictionary with health status
            
        Example:
            GET /health
            Response: {"status": "ok"}
        """
        return {"status": "ok"}
    
    return app


# Create app instance
app: FastAPI = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

