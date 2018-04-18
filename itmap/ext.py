# coding=utf-8

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
mail = Mail()
redis = FlaskRedis()
login_manager = LoginManager()
