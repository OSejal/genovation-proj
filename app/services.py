"""
Service module for integrating with Replicate API
"""
import os
from pathlib import Path
import httpx
from fastapi import HTTPException
import time
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

# Replicate API configuration from environment variables
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")
REPLICATE_API_URL = os.getenv("REPLICATE_API_URL", "https://api.replicate.com/v1/predictions")
MODEL_VERSION = os.getenv("MODEL_VERSION", "meta/llama-4-maverick-instruct")

if not REPLICATE_API_KEY:
    raise ValueError(
        f"REPLICATE_API_KEY environment variable is not set. "
        f"Please create a .env file at: {env_path}"
    )


def call_replicate_api(prompt: str, timeout: int = 60) -> str:
    """
    Send a prompt to the Replicate LLaMA model and return the response
    
    Args:
        prompt: The text prompt to send to the model
        timeout: Maximum time to wait for response (seconds)
    
    Returns:
        The model-generated text response
    
    Raises:
        HTTPException: If the API call fails
    """
    headers = {
        "Authorization": f"Token {REPLICATE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Payload for creating a prediction
    payload = {
        "version": MODEL_VERSION,
        "input": {
            "prompt": prompt
        }
    }
    
    try:
        # Step 1: Create prediction
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                REPLICATE_API_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            prediction = response.json()
        
        # Get the prediction URL and ID
        prediction_url = prediction.get("urls", {}).get("get")
        prediction_id = prediction.get("id")
        
        if not prediction_url:
            raise HTTPException(
                status_code=500,
                detail="Failed to get prediction URL from Replicate"
            )
        
        # Step 2: Poll for results
        start_time = time.time()
        with httpx.Client(timeout=30.0) as client:
            while True:
                # Check timeout
                if time.time() - start_time > timeout:
                    raise HTTPException(
                        status_code=504,
                        detail="Replicate API request timed out"
                    )
                
                # Get prediction status
                status_response = client.get(prediction_url, headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get("status")
                
                if status == "succeeded":
                    output = status_data.get("output")
                    if isinstance(output, list):
                        # Join list items into a single string
                        return "".join(output)
                    elif isinstance(output, str):
                        return output
                    else:
                        return str(output)
                
                elif status == "failed":
                    error_msg = status_data.get("error", "Unknown error")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Replicate model failed: {error_msg}"
                    )
                
                elif status == "canceled":
                    raise HTTPException(
                        status_code=500,
                        detail="Replicate prediction was canceled"
                    )
                
                # Wait before polling again
                time.sleep(1)
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Replicate API error: {e.response.text}"
        )
    
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to connect to Replicate API: {str(e)}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error calling Replicate API: {str(e)}"
        )