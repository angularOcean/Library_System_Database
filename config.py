# Citation for the following classes: Config, ProductionConfig, DevelopmentConfig
# Date: 05/17/2022
# Adapted from: Pythonise Flask Configuration Files Tutorial
# Source URL: https://pythonise.com/series/learning-flask/flask-configuration-files

from os import environ
from dotenv import load_dotenv, find_dotenv

# Load the .env file into the environment variables
load_dotenv(find_dotenv())


class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY")
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = "development"
    TESTING = True
    DEBUG = True
    DB_HOST = environ.get("LOCAL_HOST")
    DB_NAME = environ.get("LOCAL_DB")
    DB_PASSWORD = environ.get("LOCAL_PASSWORD")


class ProductionConfig(Config):
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = "production"
    DB_HOST = environ.get("MYSQL_HOST")
    DB_NAME = environ.get("MYSQL_DB")
    DB_PASSWORD = environ.get("MYSQL_PASSWORD")
    DB_USER = environ.get("MYSQL_USER")
