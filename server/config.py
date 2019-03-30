# coding=utf-8

import datetime
import os

DEBUG = False

SECRET_KEY = 'itmap@map.com'

# -- jwt --
JWT_SECRET_KEY = 'itmap@map.cn'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=60 * 60)

ITMAP_ADMINS = ['rujiazhang@foxmail.com', 'songjiyi2008@163.com']
ITMAP_ADMIN_PASSWORD = 'Aa@123456?'

# -- postgres --
DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_DATABASE = os.environ.get('DB_DATABASE', 'postgres')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE
)

# -- redis --
REDIS_URL = "redis://@redis:6379/0"

# -- email --
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ('itmap', '')

# -- avatar dir --
AVATAR_DIR = 'avatars'
ABSOLUTE_AVATAR_DIR = '/itmap/avatars/'

# -- node picture dir --
NODE_PICTURE_DIR = 'node_pictures'
ABSOLUTE_NODE_PICTURE_DIR = '/itmap/node_pictures/'

BOOK_PICTURE_DIR = 'book_pictures'
ABSOLUTE_BOOK_PICTURE_DIR = '/itmap/book_pictures/'

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "0xDH7vqsRp1VZ6wCAP7YvEf3f0ho8Ew6"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = False