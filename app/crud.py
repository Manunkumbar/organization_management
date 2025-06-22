from sqlalchemy.orm import Session
from app.models import Organization, AdminUser, OrganizationUser
from app.schemas import OrganizationCreate, AdminCreate, OrganizationUserCreate
from app.auth import get_password_hash
from typing import Optional


def create_organization(db: Session, org_data: OrganizationCreate) -> Optional[Organization]:
    """Create a new organization and its admin user"""
    try:
        # Check if organization already exists
        existing_org = db.query(Organization).filter(
            (Organization.name == org_data.organization_name) |
            (Organization.email == org_data.email)
        ).first()
        
        if existing_org:
            return None
        
        # Create database name
        db_name = f"org_{org_data.organization_name.lower().replace(' ', '_').replace('-', '_')}"
        
        # Create organization
        org = Organization(
            name=org_data.organization_name,
            email=org_data.email,
            password_hash=get_password_hash(org_data.password),
            database_name=db_name
        )
        
        db.add(org)
        db.flush()  # Get the ID without committing
        
        # Create admin user
        admin = AdminUser(
            email=org_data.email,
            password_hash=get_password_hash(org_data.password),
            organization_id=org.id
        )
        
        db.add(admin)
        db.commit()
        db.refresh(org)
        
        return org
        
    except Exception as e:
        db.rollback()
        raise e


def get_organization_by_name(db: Session, organization_name: str) -> Optional[Organization]:
    """Get organization by name"""
    return db.query(Organization).filter(Organization.name == organization_name).first()


def get_organization_by_email(db: Session, email: str) -> Optional[Organization]:
    """Get organization by email"""
    return db.query(Organization).filter(Organization.email == email).first()


def get_admin_by_email(db: Session, email: str) -> Optional[AdminUser]:
    """Get admin user by email"""
    return db.query(AdminUser).filter(AdminUser.email == email).first()


def create_organization_user(db: Session, user_data: OrganizationUserCreate) -> OrganizationUser:
    """Create a new user in an organization's database"""
    user = OrganizationUser(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_organization_user_by_email(db: Session, email: str) -> Optional[OrganizationUser]:
    """Get organization user by email"""
    return db.query(OrganizationUser).filter(OrganizationUser.email == email).first() 