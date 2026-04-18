from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.models.schema import StoryRequest, StoryResponse, ErrorResponse
from app.utils.helpers import build_prompt, validate_input
from app.config import settings
import torch
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["story"])


@router.post(
    "/generate",
    response_model=StoryResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def generate_story(request: StoryRequest, http_request: Request) -> StoryResponse:
    """
    Generate a short story based on provided parameters.
    
    This endpoint:
    1. Receives StoryRequest with name, personality, setting, theme
    2. Builds a Vietnamese prompt string
    3. Accesses model and tokenizer from app.state
    4. Generates story with creativity parameters
    5. Returns JSON with generated story
    
    Args:
        request: StoryRequest containing character details
        http_request: HTTP request object to access app.state
        
    Returns:
        StoryResponse with generated story text
        
    Raises:
        400: Invalid input (empty fields)
        503: Model not loaded
        500: AI generation error
    """
    try:
        # Get model and tokenizer from app.state
        app_state = http_request.app.state
        model = app_state.model
        tokenizer = app_state.tokenizer
        device = app_state.device
        
        # Check if model is loaded
        if model is None or tokenizer is None:
            logger.error("Model or tokenizer is None")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model is not loaded. Please check server logs."
            )
        
        # Validate input
        request_dict = request.model_dump()
        if not validate_input(request_dict):
            logger.warning(f"Invalid input received: {request_dict}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid input: All fields must be non-empty strings"
            )
        
        # Build prompt from request
        prompt = build_prompt(request)
        logger.info(f"Generated prompt: {prompt}")
        
        # Encode prompt to input IDs
        logger.info("Encoding prompt...")
        input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
        logger.info(f"Input shape: {input_ids.shape}")
        
        # Generate story with specified parameters
        logger.info("Generating story with model...")
        with torch.no_grad():
            output_ids = model.generate(
                input_ids,
                max_new_tokens=150,           # Generate up to 150 new tokens
                temperature=0.8,               # Control randomness (0.7-0.9 is good for creativity)
                top_p=0.9,                    # Nucleus sampling for diversity
                do_sample=True,                # Enable sampling for varied outputs
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
                num_return_sequences=1        # Generate only 1 story
            )
        
        logger.info(f"Generated output shape: {output_ids.shape}")
        
        # Decode output to UTF-8 Vietnamese string
        logger.info("Decoding output to text...")
        generated_text = tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True,
            clean_up_tokenizer_space=True
        )
        
        # Extract only the story part (remove the prompt)
        # The generated_text includes the prompt, so we remove it
        if generated_text.startswith(prompt):
            story_part = generated_text[len(prompt):].strip()
        else:
            # Fallback if prompt is not at the beginning
            story_part = generated_text.replace(prompt, "", 1).strip()
        
        logger.info(f"Generated story ({len(story_part)} chars): {story_part[:100]}...")
        
        # Return success response
        return StoryResponse(
            status="success",
            story=story_part,
            message="Story generated successfully"
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions (400, 503, etc.)
        raise
    
    except Exception as e:
        # Catch all other exceptions and return 500 error
        error_message = str(e)
        logger.error(f"Error during story generation: {error_message}", exc_info=True)
        
        # Return JSON error response with 500 status
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": error_message,
                "status": "error"
            }
        )


@router.get("/health")
async def health_check(request: Request):
    """Health check endpoint with model status"""
    app_state = request.app.state
    
    return {
        "status": "healthy",
        "model_loaded": app_state.model is not None,
        "device": getattr(app_state, 'device', 'unknown')
    }

