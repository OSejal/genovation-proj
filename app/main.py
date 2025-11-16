"""
Main FastAPI application
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from .models import (
    LoginRequest, LoginResponse, PromptRequest, PromptResponse,
    HistoryResponse, HistoryItem, ErrorResponse
)
from .auth import authenticate_user, verify_token
from .services import call_replicate_api
from .storage import add_to_history, get_user_history

# Create FastAPI app
app = FastAPI(
    title="LLaMA Prompt API",
    description="FastAPI backend for submitting prompts to LLaMA model via Replicate",
    version="1.0.0"
)

# CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to LLaMA Prompt API",
        "version": "1.0.0",
        "endpoints": {
            "POST /login/": "Authenticate and get token",
            "POST /prompt/": "Submit prompt to LLaMA model (requires auth)",
            "GET /history/": "Get your prompt history (requires auth)"
        },
        "docs": "/docs"
    }


@app.post("/login/", response_model=LoginResponse, tags=["Authentication"])
def login(request: LoginRequest):
    """
    Authenticate user and return access token
    
    - **username**: Your username
    - **password**: Your password
    
    Returns a bearer token to use in subsequent requests
    """
    token = authenticate_user(request.username, request.password)
    
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    return LoginResponse(
        token=token,
        message=f"Login successful. Welcome, {request.username}!"
    )


@app.post("/prompt/", response_model=PromptResponse, tags=["Prompts"])
def submit_prompt(
    request: PromptRequest,
    username: str = Depends(verify_token)
):
    """
    Submit a prompt to the LLaMA model and get a response
    
    - **prompt**: Your prompt text for the AI model
    
    Requires: Authorization header with Bearer token
    """
    # Call Replicate API
    try:
        model_response = call_replicate_api(request.prompt)
    except HTTPException as e:
        # Re-raise HTTP exceptions from the service
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing prompt: {str(e)}"
        )
    
    timestamp = datetime.now().isoformat()
    
    add_to_history(username, request.prompt, model_response)
    
    return PromptResponse(
        prompt=request.prompt,
        response=model_response,
        timestamp=timestamp
    )


@app.get("/history/", response_model=HistoryResponse, tags=["History"])
def get_history(username: str = Depends(verify_token)):
    """
    Get your prompt history
    
    Returns all your previously submitted prompts and their responses
    
    Requires: Authorization header with Bearer token
    """
    # Get user's history
    user_history = get_user_history(username)
    
    # Convert to Pydantic models
    history_items = [
        HistoryItem(
            timestamp=item["timestamp"],
            prompt=item["prompt"],
            response=item["response"]
        )
        for item in user_history
    ]
    
    return HistoryResponse(
        username=username,
        history=history_items,
        total_prompts=len(history_items)
    )


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }