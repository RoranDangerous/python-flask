import os
import datetime
DATABASE_URL = os.environ.get('DATABASE_URL')

class JWTConfig:
    """ JWT Token Configuration """
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_HEADER_TYPE = 'JWT'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)

class BaseConfig(JWTConfig):
    """ Base Configuration """
    SECRET_KEY =  os.getenv('SECRET_KEY')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """ Development Configuration """
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

class TestingConfig(BaseConfig):
    """ Testing Configuration """
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = DATABASE_URL + "_test"
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProductionConfig(BaseConfig):
    """ Production configuration """
    SECRET_KEY = ''
    SQLALCHEMY_DATABASE_URI = ''