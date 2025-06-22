from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_master_db, create_organization_database
from app.crud import create_organization, get_organization_by_name
from app.schemas import OrganizationCreate, OrganizationResponse
from typing import List

router = APIRouter(prefix="/org", tags=["organizations"])


@router.post("/create", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization_endpoint(
    org_data: OrganizationCreate,
    db: Session = Depends(get_master_db)
):
    """
    Create a new organization with admin user and dynamic database
    """
    try:
        # Create organization in master database
        organization = create_organization(db, org_data)
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization with this name or email already exists"
            )
        
        # Create dynamic database for the organization
        db_created = create_organization_database(org_data.organization_name)
        
        if not db_created:
            # If database creation fails, we should clean up the organization
            # For now, we'll just return an error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create organization database"
            )
        
        return organization
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create organization: {str(e)}"
        )


@router.get("/get", response_model=OrganizationResponse)
def get_organization_by_name_endpoint(
    organization_name: str,
    db: Session = Depends(get_master_db)
):
    """
    Get organization by name
    """
    organization = get_organization_by_name(db, organization_name)
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    return organization


@router.get("/list", response_model=List[OrganizationResponse])
def list_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_master_db)
):
    """
    List all organizations (for admin purposes)
    """
    from app.models import Organization
    
    organizations = db.query(Organization).offset(skip).limit(limit).all()
    return organizations 