import os
import urllib

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'superSecretPass'
    # SERVER_NAME = "192.168.1.165:5000"
    # SERVER_NAME = "localhost:5000"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./DataBase/projetoTFC.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

