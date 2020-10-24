from os import path, environ

# Define the application directory
BASE_DIR = path.abspath(path.dirname(__file__))  

class DevConfig(object):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "secret"

class ProductionConfig(DevConfig):
    DEBUG = False
    DEVELOPMENT = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql:///' + path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY')