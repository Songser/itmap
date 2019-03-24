# coding=utf-8

import datetime
import os

DEBUG = False

SECRET_KEY = '...'

# -- jwt --
JWT_SECRET_KEY = '...'
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