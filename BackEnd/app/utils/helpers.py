import logging
from typing import Dict
from app.models.schema import StoryRequest

logger = logging.getLogger(__name__)


def build_prompt(request: StoryRequest) -> str:
    """
    Build a formatted Vietnamese prompt from StoryRequest model.
    
    Args:
        request: StoryRequest containing name, personality, setting, theme
        
    Returns:
        Formatted prompt string in Vietnamese
    """
    prompt = (
        f"Nhân vật: {request.name} | "
        f"Tính cách: {request.personality} | "
        f"Bối cảnh: {request.setting} | "
        f"Chủ đề: {request.theme}. Truyện: "
    )
    return prompt


def validate_input(data: Dict[str, str]) -> bool:
    """
    Validate input data
    
    Args:
        data: Dictionary containing story parameters
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['name', 'personality', 'setting', 'theme']
    
    for field in required_fields:
        if field not in data or not isinstance(data[field], str) or len(data[field].strip()) == 0:
            logger.warning(f"Missing or empty field: {field}")
            return False
    
    return True
