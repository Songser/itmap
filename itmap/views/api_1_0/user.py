# coding=utf-8

from collections import OrderedDict
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
)

from itmap.models.user import User


class UserApi(Resource):

    method_decorators = [jwt_required]

    def get(self, uid):
        user = User.query.get(uid)
        if not user:
            return {'msg': 'Invalid args'}, 400
        return user.to_dict, 200
