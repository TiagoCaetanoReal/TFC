import os
import urllib

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'superSecretPass' 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./DataBase/projetoTFC.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    BABEL_TRANSLATION_DIRECTORIES = 'wtforms:translations'
    BABEL_DEFAULT_LOCALE = 'pt'


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

