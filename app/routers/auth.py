from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_master_db
from app.crud import get_admin_by_email
from app.auth import authenticate_admin, create_access_token, get_current_admin
from app.schemas import AdminLogin, Token
from datetime import timedelta
from app.config import settings

router = APIRouter(prefix="/admin", tags=["authentication"])


@router.post("/login", response_model=Token)
def login_for_access_token(
    admin_credentials: AdminLogin,
    db: Session = Depends(get_master_db)
):
    """
    Login for admin users and get JWT token
    """
    # Authenticate admin
    admin = authenticate_admin(db, admin_credentials.email, admin_credentials.password)
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get organization name for the admin
    organization_name = admin.organization.name
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": admin.email, "org": organization_name},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_email": admin.email,
        "organization_name": organization_name
    }


@router.get("/me")
def read_admin_me(current_admin = Depends(get_current_admin)):
    """
    Get current admin information
    """
    return {
        "id": current_admin.id,
        "email": current_admin.email,
        "organization_id": current_admin.organization_id,
        "organization_name": current_admin.organization.name
    } 