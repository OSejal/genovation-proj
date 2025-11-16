"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class LoginRequest(BaseModel):
    """Request model for login endpoint"""
    username: str = Field(..., description="Username for authentication")
    password: str = Field(..., description="Password for authentication")


class LoginResponse(BaseModel):
    """Response model for successful login"""
    token: str = Field(..., description="Authentication token")
    message: str = Field(default="Login successful")


class PromptRequest(BaseModel):
    """Request model for submitting a prompt"""
    prompt: str = Field(..., min_length=1, description="Prompt text to send to the model")


class PromptResponse(BaseModel):
    """Response model for prompt submission"""
    prompt: str = Field(..., description="Original prompt submitted")
    response: str = Field(..., description="Model-generated response")
    timestamp: str = Field(..., description="Timestamp of the request")


class HistoryItem(BaseModel):
    """Model for a single history record"""
    timestamp: str = Field(..., description="When the prompt was submitted")
    prompt: str = Field(..., description="The prompt text")
    response: str = Field(..., description="The model's response")


class HistoryResponse(BaseModel):
    """Response model for history endpoint"""
    username: str = Field(..., description="Username whose history this is")
    history: List[HistoryItem] = Field(default_factory=list, description="List of prompt/response pairs")
    total_prompts: int = Field(..., description="Total number of prompts in history")


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str = Field(..., description="Error message")