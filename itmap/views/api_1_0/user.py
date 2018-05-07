# coding=utf-8

import os

from flask import request
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
)

from itmap.models.user import User


class UserApi(Resource):

    method_decorators = [jwt_required]

    def get(self, uid):
        """
        file: swagger/user.yml
        """
        user = User.query.get(uid)
        if not user:
            return {'msg': 'Invalid args'}, 400
        return user.to_dict, 200


class UserAvatarApi(Resource):

    method_decorators = [jwt_required]

    def put(self, uid):
        """
        file: swagger/user_avatar_put.yml
        """
        user = User.query.get(uid)
        if not user:
            return {'msg': 'Invalid args'}, 400
        path = user.avatar
        with open(path, 'wb') as fp:
            fp.write(request.get_data())
        return '', 201

    def delete(self, uid):
        """
        file: swagger/user_avatar_delete.yml
        """
        user = User.query.get(uid)
        if not user:
            return {'msg': 'Invalid args'}, 400
        path = user.avatar
        if not os.path.isfile(path):
            return {'msg': 'Upload Avatar first'}, 400
        os.remove(path)
        return '', 204
