# coding=utf-8

import datetime

DEBUG = False

SECRET_KEY = '...'

# -- jwt --
JWT_SECRET_KEY = '...'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=60 * 60)

ITMAP_ADMINS = ['rujiazhang@foxmail.com', 'songjiyi2008@163.com']
ITMAP_ADMIN_PASSWORD = 'Aa@123456?'

# -- postgres --
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@postgres:5432/postgres"

# -- redis --
REDIS_URL = "redis://@redis:6379/0"

# -- email --
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ('itmap', '')
