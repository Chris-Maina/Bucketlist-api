# /instance/config.py

import os

class Config(object):
    """Parent config class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = "hardworkpayseverytime"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:chris@localhost:5432/flask_api"

class DevelopmentConfig(Config):
    """Configs for development"""
    DEBUG = True

class TestingConfig(Config):
    """Configs for testing, with a separate test db"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:chris@localhost:5432/test_db"
    DEBUG = True

class StagingConfig(Config):
    """Configs for staging"""
    DEBUG = True

class ProductionConfig(Config):
    """Configs for production"""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
