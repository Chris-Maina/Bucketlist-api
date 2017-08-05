# /instance/config.py


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
    SQLALCHEMY_DATABASE_URI = "postgres://yroreitiyrpffu:a31393a9e7006ea18452376c29c599d5051e6f38fe56d3cc59c81ef262dba4b5@ec2-54-227-252-202.compute-1.amazonaws.com:5432/dbpp9omfchlvo6"


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
