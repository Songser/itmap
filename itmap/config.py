# coding=utf-8

# import datetime

DEBUG = False

SECRET_KEY = '...'
JWT_SECRET_KEY = '...'

# JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=60 * 60 * 24)

ITMAP_ADMINS = ['rujiazhang@foxmail.com', 'songjiyi2008@163.com']
ITMAP_ADMIN_PASSWORD = 'Aa@123456?'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@postgres:5432/postgres"

REDIS_URL = "redis://@redis:6379/0"
