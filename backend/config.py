# backend/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    DEBUG = False
    TESTING = False
    # Add other common configurations

class DevelopmentConfig(Config):
    DEBUG = True
    # Development-specific configurations

class TestingConfig(Config):
    TESTING = True
    # Testing-specific configurations

class ProductionConfig(Config):
    # Production-specific configurations
    pass
