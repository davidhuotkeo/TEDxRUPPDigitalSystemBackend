import os
from app import app

class BaseConfig:
    SECRET_KEY = "pXx3wumu67tJV58r"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QRCODE_PASSWORD = "c028bf8b4632bbf6b691d062a5482984fea8b4d6dc2ad4913cd7082d552b"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Davidhuotkeo123@localhost/tedcircletest"

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Davidhuotkeo123@localhost/tedcircle"

configs = {
    "default": BaseConfig,
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}
