# coding=utf-8

from collections import OrderedDict

from flask import request
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
)

from itmap.ext import db
from itmap.models.graph import Node
from itmap.utils import update


class NodeApi(Resource):

    method_decorators = [jwt_required]

    def put(self, nid):
        node = Node.query.get(nid)
        uid = get_jwt_identity()
        data = request.json
        data = dict(data)
        if node is None:
            if not (data.get('graph_id') and data.get('name')):
                return {'msg': 'Invalid args'}, 400
            data.update({
                'owner_id': uid,
            })
            node = Node(**data)
        elif node.owner_id != uid:
            return {'msg': 'Not allowed to put'}, 400
        else:
            update(node, data)
        db.session.add(node)
        db.session.commit()
        return node.id, 200

    def delete(self, nid):
        node = Node.query.get(nid)
        if node is None:
            return {'msg': 'Invalid nid'}, 400
        db.session.delete(node)
        db.session.commit()
        return '', 200
