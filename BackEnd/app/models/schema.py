from pydantic import BaseModel, Field
from typing import Optional


class StoryRequest(BaseModel):
    """Request body for story generation"""
    name: str = Field(..., min_length=1, max_length=100, description="Character name")
    personality: str = Field(..., min_length=1, max_length=100, description="Character personality")
    setting: str = Field(..., min_length=1, max_length=100, description="Story setting")
    theme: str = Field(..., min_length=1, max_length=100, description="Story theme")


class StoryResponse(BaseModel):
    """Response body for story generation"""
    status: str = Field(..., description="Status of the request: 'success' or 'error'")
    story: str = Field(..., description="Generated short story")
    message: Optional[str] = Field(None, description="Additional message or error details")


class ErrorResponse(BaseModel):
    """Response body for errors"""
    error: str = Field(..., description="Error message describing what went wrong")
    status: str = Field(default="error", description="Status indicator: always 'error'")
