from fastapi import APIRouter, HTTPException, Request, status
from app.models.schema import StoryRequest, StoryResponse, ErrorResponse
from app.utils.helpers import (
    build_fallback_story,
    build_creative_direction,
    build_prompt,
    clean_generated_story,
    detect_language,
    extract_story_text,
    is_story_quality_acceptable,
    score_story_candidate,
    validate_input,
)
import torch
import random
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
    2. Detects language (Vietnamese/English) from user input
    3. Tries model generation
    4. Falls back to deterministic complete story if model output is low quality
    5. Returns JSON with generated story
    
    Args:
        request: StoryRequest containing character details
        http_request: HTTP request object to access app.state
        
    Returns:
        StoryResponse with generated story text
        
    Raises:
        400: Invalid input (empty fields)
        500: AI generation error
    """
    try:
        # Get model and tokenizer from app.state
        app_state = http_request.app.state
        model = app_state.model
        tokenizer = app_state.tokenizer
        device = app_state.device
        
        # Validate input
        request_dict = request.model_dump()
        if not validate_input(request_dict):
            logger.warning(f"Invalid input received: {request_dict}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid input: All fields must be non-empty strings"
            )
        
        # Detect output language from user descriptions
        language = detect_language(request_dict)

        # Build prompt from request
        prompt = build_prompt(request, language=language)
        prompt += build_creative_direction(request, language)
        logger.info("Detected language: %s", language)
        logger.info("Generated prompt: %s", prompt)

        story_part = ""
        generation_used = False
        max_attempts = 2
        best_candidate = ""
        best_score = -10_000

        # Try model generation when model/tokenizer are available
        if model is not None and tokenizer is not None:
            for attempt in range(1, max_attempts + 1):
                try:
                    # Reset random seed before each attempt to ensure diverse outputs
                    # across different requests (prevents model from repeating the same story)
                    rand_seed = random.randint(0, 2**31 - 1)
                    torch.manual_seed(rand_seed)
                    if torch.cuda.is_available():
                        torch.cuda.manual_seed_all(rand_seed)
                    logger.info("Attempt %s using seed %s", attempt, rand_seed)

                    logger.info("Encoding prompt for attempt %s...", attempt)
                    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
                    logger.info("Input shape: %s", input_ids.shape)

                    logger.info("Generating story with model (attempt %s/%s)...", attempt, max_attempts)
                    with torch.no_grad():
                        output_ids = model.generate(
                            input_ids,
                            max_new_tokens=280,
                            temperature=1.05 + (attempt - 1) * 0.10,
                            top_p=min(0.97, 0.95 + attempt * 0.02),
                            top_k=100,
                            do_sample=True,
                            repetition_penalty=1.15,
                            no_repeat_ngram_size=3,
                            pad_token_id=tokenizer.pad_token_id,
                            eos_token_id=tokenizer.eos_token_id,
                            num_return_sequences=3,
                        )

                    logger.info("Generated output shape: %s", output_ids.shape)
                    for output_id in output_ids:
                        generated_text = tokenizer.decode(
                            output_id,
                            skip_special_tokens=True,
                            clean_up_tokenization_spaces=True,
                        )
                        candidate_story = clean_generated_story(
                            extract_story_text(generated_text, prompt)
                        )
                        candidate_score = score_story_candidate(candidate_story, language, request)
                        logger.info("Candidate score on attempt %s: %s", attempt, candidate_score)

                        if candidate_score > best_score:
                            best_score = candidate_score
                            best_candidate = candidate_story

                        if (
                            candidate_score >= 55
                            and is_story_quality_acceptable(candidate_story, language, request)
                        ):
                            story_part = candidate_story
                            generation_used = True
                            logger.info("Accepted model output on attempt %s", attempt)
                            break

                    if generation_used:
                        break

                    logger.warning("No strong candidate on attempt %s", attempt)
                except Exception as gen_error:
                    logger.warning("Model generation failed on attempt %s: %s", attempt, str(gen_error))
        else:
            logger.warning("Model or tokenizer not available, using fallback story generator")

        # Prefer the model's best draft over template fallback when it is readable.
        if not generation_used and best_candidate and best_score >= 40:
            logger.warning("Using best creative model draft with score %s.", best_score)
            story_part = best_candidate
            generation_used = True

        # Safety net: ensure user always gets a complete, readable story.
        if not generation_used:
            logger.warning("No acceptable model output after %s attempts. Using fallback story builder.", max_attempts)
            story_part = build_fallback_story(request, language)
            generation_used = False

        logger.info("Final story (%s chars): %s...", len(story_part), story_part[:100])
        
        # Return success response
        return StoryResponse(
            status="success",
            story=story_part,
            message=(
                f"Story generated successfully in {'Vietnamese' if language == 'vi' else 'English'}"
                if generation_used
                else f"Story generated with fallback in {'Vietnamese' if language == 'vi' else 'English'}"
            ),
        )
    
    except HTTPException:
        # Re-raise explicit HTTP exceptions (400, etc.)
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

