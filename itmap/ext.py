# coding=utf-8

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = ''
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy()
mail = Mail()
redis = FlaskRedis()
login_manager = LoginManager()
