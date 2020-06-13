import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # FLASK_ADMIN_SWATCH = 'cerulean'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://neighborrow:pass@localhost:5432/neighborrow"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # set true to log db access

    SECRET_KEY = 'this-really-needs-to-be-changed'

    JTW_SECRET_KEY = 'this-also-needs-to-be-changed'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class TestingConfig(Config):
    TESTING = True
