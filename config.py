import os

class Config:
   SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:slowwhine@localhost/pitchy'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class DevConfig(Config):
    DEBUG = True

# class TestConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:slowwhine@localhost/pitchy_test'

config_options = {
    'development':DevConfig,
    'production':ProdConfig,
    # 'test':TestConfig
}

