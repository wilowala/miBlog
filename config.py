from distutils.debug import DEBUG
import os

from click import confirmation_option

DB_NAME = "database.db"

class Config:
    SECRET_KEY = 'secretkey'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
    
    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    
class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG=True
    pass
class TestConfig(Config):
    pass
config_options = {
    'development' : DevConfig,
    'production_mode' :ProdConfig,
    'testing' : TestConfig
}