from fastapi import APIRouter, HTTPException, status
from app.models.schema import StoryRequest, StoryResponse, ErrorResponse
from app.models.model_loader import model_loader
from app.utils.helpers import construct_prompt, validate_input
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["story"])


@router.post(
    "/generate",
    response_model=StoryResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def generate_story(request: StoryRequest) -> StoryResponse:
    """
    Generate a short story based on provided parameters
    
    Args:
        request: StoryRequest containing name, personality, setting, theme
        
    Returns:
        StoryResponse with generated story
    """
    try:
        # Validate input
        request_dict = request.model_dump()
        if not validate_input(request_dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid input: All fields must be non-empty strings"
            )
        
        # Construct prompt
        prompt = construct_prompt(request_dict)
        logger.info(f"Generated prompt: {prompt}")
        
        # Generate story
        story = model_loader.generate_story(
            prompt=prompt,
            max_length=settings.max_length,
            device=settings.device
        )
        
        # Return only the generated part (remove the prompt)
        generated_part = story.replace(prompt, "", 1).strip()
        
        return StoryResponse(
            status="success",
            story=generated_part,
            message="Story generated successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating story: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "app": settings.app_name, "version": settings.app_version}
