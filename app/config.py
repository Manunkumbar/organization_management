from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Master Database Configuration
    master_db_url: str = "postgresql://postgres:password@localhost:5432/master_db"
    
    # JWT Configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Organization Database Configuration
    org_db_host: str = "localhost"
    org_db_port: int = 5432
    org_db_user: str = "postgres"
    org_db_password: str = "password"
    org_db_template: str = "template0"
    
    class Config:
        env_file = ".env"


settings = Settings() 