from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Master Database Engine
master_engine = create_engine(settings.master_db_url)
MasterSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=master_engine)

# Base class for models
Base = declarative_base()


def get_master_db():
    """Get master database session"""
    db = MasterSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_organization_database(org_name: str) -> bool:
    """Create a new database for an organization"""
    try:
        # Create a connection to PostgreSQL server (not a specific database)
        server_url = f"postgresql://{settings.org_db_user}:{settings.org_db_password}@{settings.org_db_host}:{settings.org_db_port}/postgres"
        server_engine = create_engine(server_url)
        
        with server_engine.connect() as conn:
            # Create the organization database
            db_name = f"org_{org_name.lower().replace(' ', '_').replace('-', '_')}"
            conn.execute(text(f"CREATE DATABASE {db_name} TEMPLATE {settings.org_db_template}"))
            conn.commit()
            
            # Create organization-specific engine and tables
            org_db_url = f"postgresql://{settings.org_db_user}:{settings.org_db_password}@{settings.org_db_host}:{settings.org_db_port}/{db_name}"
            org_engine = create_engine(org_db_url)
            
            # Create tables in the organization database
            Base.metadata.create_all(bind=org_engine)
            
            logger.info(f"Created organization database: {db_name}")
            return True
            
    except Exception as e:
        logger.error(f"Error creating organization database: {e}")
        return False


def get_organization_db(org_name: str):
    """Get organization-specific database session"""
    try:
        db_name = f"org_{org_name.lower().replace(' ', '_').replace('-', '_')}"
        org_db_url = f"postgresql://{settings.org_db_user}:{settings.org_db_password}@{settings.org_db_host}:{settings.org_db_port}/{db_name}"
        org_engine = create_engine(org_db_url)
        OrgSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=org_engine)
        
        db = OrgSessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error connecting to organization database: {e}")
        raise 