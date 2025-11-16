"""
Authentication module for token-based authentication
"""
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import secrets

# Security scheme for Bearer token
security = HTTPBearer()

# Hardcoded users with their tokens
USERS_DB = {
    "user1": {
        "password": "pass1",
        "token": "token_user1_abc123"
    },
    "user2": {
        "password": "pass2",
        "token": "token_user2_xyz789"
    },
    "admin": {
        "password": "admin123",
        "token": "token_admin_secure456"
    }
}

# Reverse lookup: token -> username
TOKENS_DB = {user_data["token"]: username for username, user_data in USERS_DB.items()}


def authenticate_user(username: str, password: str) -> Optional[str]:
    """
    Authenticate user and return token if valid
    
    Args:
        username: User's username
        password: User's password
    
    Returns:
        Token string if authentication successful, None otherwise
    """
    user = USERS_DB.get(username)
    if user and user["password"] == password:
        return user["token"]
    return None


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verify the Bearer token and return the username
    
    Args:
        credentials: HTTP Authorization credentials from request header
    
    Returns:
        Username associated with the token
    
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    username = TOKENS_DB.get(token)
    
    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return username