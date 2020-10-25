import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLACHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('PLUMMY')

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:slowwhine@localhost/pitchy'
    DEBUG = True

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:slowwhine@localhost/pitchy_test'

config_options = {
    'development':DevConfig,
    'production':ProdConfig,
    'test':TestConfig
}

