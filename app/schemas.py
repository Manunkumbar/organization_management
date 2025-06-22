from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Organization Schemas
class OrganizationCreate(BaseModel):
    email: EmailStr
    password: str
    organization_name: str


class OrganizationResponse(BaseModel):
    id: int
    name: str
    email: str
    database_name: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


# Admin User Schemas
class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    organization_name: str


class AdminResponse(BaseModel):
    id: int
    email: str
    organization_id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user_email: str
    organization_name: str


class TokenData(BaseModel):
    email: Optional[str] = None
    organization_name: Optional[str] = None


# Organization User Schemas
class OrganizationUserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str = "user"


class OrganizationUserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True 