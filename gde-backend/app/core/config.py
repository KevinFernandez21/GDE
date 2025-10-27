"""
Configuration settings for the GDE Backend API.
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
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
    
    # CORS - stored as strings, converted to lists via computed fields
    _allowed_origins_str: str = "http://localhost:3000"
    _allowed_methods_str: str = "GET,POST,PUT,DELETE,PATCH"
    _allowed_headers_str: str = "*"
    
    # File Upload
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB
    _allowed_file_types_str: str = "csv,xlsx,xls,json"
    
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
    
    @computed_field
    @property
    def allowed_origins(self) -> List[str]:
        """Parse allowed origins from environment variable."""
        env_val = os.getenv("ALLOWED_ORIGINS", self._allowed_origins_str)
        return [i.strip() for i in env_val.split(",") if i.strip()]
    
    @computed_field
    @property
    def allowed_methods(self) -> List[str]:
        """Parse allowed methods from environment variable."""
        env_val = os.getenv("ALLOWED_METHODS", self._allowed_methods_str)
        return [i.strip() for i in env_val.split(",") if i.strip()]
    
    @computed_field
    @property
    def allowed_headers(self) -> List[str]:
        """Parse allowed headers from environment variable."""
        env_val = os.getenv("ALLOWED_HEADERS", self._allowed_headers_str)
        return [i.strip() for i in env_val.split(",") if i.strip()]
    
    @computed_field
    @property
    def allowed_file_types(self) -> List[str]:
        """Parse allowed file types from environment variable."""
        env_val = os.getenv("ALLOWED_FILE_TYPES", self._allowed_file_types_str)
        return [i.strip() for i in env_val.split(",") if i.strip()]


# Global settings instance
settings = Settings()
