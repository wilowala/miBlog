import os 

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

class Config:
    SECRET_KEY=os.urandom(346)    
    SQLALCHEMY_TRACK_MODIFICATIONS  = False

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI="postgresql://fimpksjcpwzlaj:4a65b728269f400d3b4b71641c9f63195bbf3a0b6a474a1d47b31740b31cc855@ec2-54-86-224-85.compute-1.amazonaws.com:5432/dfpbu5qncc2rd6"
    # os.getenv("DATABASE_URL").replace('postgres://', 'postgresql://')
    # print(SQLALCHEMY_DATABASE_URI)
class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI ="postgresql://fimpksjcpwzlaj:4a65b728269f400d3b4b71641c9f63195bbf3a0b6a474a1d47b31740b31cc855@ec2-54-86-224-85.compute-1.amazonaws.com:5432/dfpbu5qncc2rd6"
    # os.getenv("SQLALCHEMY_DATABASE_URI")

config_options = {
    'dev': DevConfig,
    'prod': ProdConfig
}