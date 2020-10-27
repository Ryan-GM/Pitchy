import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:slowwhine@localhost/pitchy'
    SQLACHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('PLUMMY')
    #simple mde configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    #email configurations
    MAIL_SERVER = 'smtp.googleemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

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

