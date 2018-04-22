# coding=utf-8

from collections import OrderedDict
from flask_restful import Resource, fields, marshal, marshal_with, reqparse

from itmap.models.user import User, Role


class UserApi(Resource):
    def get(self):
        pass

    def put(self):
        pass
