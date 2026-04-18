import logging
from typing import Dict

logger = logging.getLogger(__name__)


def construct_prompt(data: Dict[str, str]) -> str:
    """
    Construct a prompt from the request data
    
    Args:
        data: Dictionary containing name, personality, setting, theme
        
    Returns:
        Formatted prompt string
    """
    prompt = (
        f"Nhân vật: {data['name']} | "
        f"Tính cách: {data['personality']} | "
        f"Bối cảnh: {data['setting']} | "
        f"Chủ đề: {data['theme']}. Câu chuyện: "
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
