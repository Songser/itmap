# coding=utf-8

import os

from flask import request, current_app
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
        current_uid = get_jwt_identity()
        if current_uid != uid:
            return {'msg': 'Not allowed'}, 400
        user = User.query.get(uid)
        path = user.avatar
        f = request.files['avatar']
        f.save(path)
        #current_app.logger.error(request.get_data())
        # with open(path, 'wb') as fp:
            # fp.write(request.get_data())
        return '', 201

    def delete(self, uid):
        """
        file: swagger/user_avatar_delete.yml
        """
        current_uid = get_jwt_identity()
        if current_uid != uid:
            return {'msg': 'Not allowed'}, 400
        user = User.query.get(uid)
        path = user.avatar
        if not os.path.isfile(path):
            return {'msg': 'Upload Avatar first'}, 400
        os.remove(path)
        return '', 204
