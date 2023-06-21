import os
import urllib

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'superSecretPass'
    # SERVER_NAME = "loscalhost:5000"
    params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=DESKTOP-56CVD06\MSSQLSERVER01;DATABASE=projetoTFC;Trusted_Connection=yes;')
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True