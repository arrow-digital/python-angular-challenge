"""
Configuration module for OpenBanking Services API Client

This module contains configuration settings and environment variables
for the OpenBanking API client application.
"""

import os
from typing import Optional


class Config:
    """Base configuration class."""

    # OpenBanking API Configuration
    OPENBANKING_BASE_URL = os.getenv(
        'OPENBANKING_BASE_URL',
        'http://localhost:7004/open-banking/products-services/v2'
    )

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # Request Configuration
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))

    # Pagination Configuration
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', '25'))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', '100'))

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    LOG_LEVEL = 'WARNING'

    # Security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

    # Use in-memory or test database
    OPENBANKING_BASE_URL = 'http://localhost:7004/open-banking/products-services/v2'


def get_config(environment: Optional[str] = None) -> Config:
    """
    Get configuration based on environment.

    Args:
        environment: Environment name (development, production, testing)

    Returns:
        Configuration object
    """
    if environment is None:
        environment = os.getenv('FLASK_ENV', 'development')

    config_mapping = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }

    return config_mapping.get(environment, DevelopmentConfig)()
