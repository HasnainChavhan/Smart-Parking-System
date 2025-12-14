"""
Authentication endpoints for user registration, login, and token management.
"""

from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uuid

from app.core import security
from app.core.config import settings
from app.db import models, session
from app.schemas import schemas
from loguru import logger

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(session.get_db)):
    """
    Register a new user.
    
    - **email**: Valid email address
    - **password**: Strong password (min 8 characters)
    - **name**: User's full name
    """
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = security.get_password_hash(user_data.password)
    new_user = models.User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"New user registered: {new_user.email}")
    
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(session.get_db)
):
    """
    Login with email and password to get access token.
    
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = security.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        logger.warning(f"Failed login attempt for: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = security.create_access_token(data={"sub": user.id})
    refresh_token = security.create_refresh_token(data={"sub": user.id})
    
    logger.info(f"User logged in: {user.email}")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: str, db: Session = Depends(session.get_db)):
    """
    Refresh access token using refresh token.
    """
    try:
        payload = security.decode_token(refresh_token)
        token_type = payload.get("type")
        
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        user = db.query(models.User).filter(models.User.id == user_id).first()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new tokens
        new_access_token = security.create_access_token(data={"sub": user.id})
        new_refresh_token = security.create_refresh_token(data={"sub": user.id})
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(
    current_user: models.User = Depends(security.get_current_active_user)
):
    """
    Get current user information.
    """
    return current_user


@router.post("/logout")
def logout(current_user: models.User = Depends(security.get_current_active_user)):
    """
    Logout current user.
    
    Note: In a production system, you would typically:
    1. Add the token to a blacklist/revocation list
    2. Store blacklisted tokens in Redis with expiration
    3. Check blacklist on each request
    
    For now, this is a placeholder that confirms logout.
    Client should delete the token from storage.
    """
    logger.info(f"User logged out: {current_user.email}")
    return {"message": "Successfully logged out"}
