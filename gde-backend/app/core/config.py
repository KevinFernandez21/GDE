"""
Configuration settings for the GDE Backend API.
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "GDE Backend API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # Database
    database_url: str
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    allowed_headers: List[str] = ["*"]
    
    # File Upload
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB
    allowed_file_types: List[str] = ["csv", "xlsx", "xls", "json"]
    
    # Email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_tls: bool = True
    
    # Notifications
    fcm_server_key: Optional[str] = None
    webhook_url: Optional[str] = None
    
    # External Services
    openai_api_key: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Rate Limiting
    rate_limit_requests: int = 1000
    rate_limit_window: int = 3600  # 1 hour
    
    # Cache
    redis_url: Optional[str] = None
    cache_ttl: int = 300  # 5 minutes
    
    @validator("allowed_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("allowed_methods", pre=True)
    def parse_cors_methods(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("allowed_file_types", pre=True)
    def parse_file_types(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
