# coding=utf-8

import os

from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
)

from itmap.ext import db
from itmap.models.graph import Node, Graph
from itmap.utils import update

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', trim=True)
parser.add_argument('relate_page_url')
parser.add_argument('is_template', type=bool)
parser.add_argument('color')
parser.add_argument('size', choices=('S', 'M', 'L'), help='Bad choice: {error_msg}')
parser.add_argument('shape', choices=('circle', 'triangle', 'roundRect', 'diamond'), help='Bad choice: {error_msg}')
parser.add_argument('graph_id', type=int, required=True)
parser.add_argument('description')


class NodePostApi(Resource):

    method_decorators = [jwt_required]

    def post(self):
        """
        file: swagger/node_post.yml
        """
        uid = get_jwt_identity()
        vals = dict(parser.parse_args())
        graph = Graph.query.get(vals['graph_id'])
        if not (graph and graph.owner_id == uid):
            return {'msg': 'Not allowed to post'}, 400
        vals.update({
            'owner_id': uid,
        })
        node = Node(**vals)
        db.session.add(node)
        db.session.commit()
        return node.id, 201


class NodeApi(Resource):

    method_decorators = [jwt_required]

    def put(self, nid):
        """
        file: swagger/node_put.yml
        """
        node = Node.query.get(nid)
        uid = get_jwt_identity()
        if node is None:
            return {'msg': 'Invalid nid'}, 400
        elif node.owner_id != uid:
            return {'msg': 'Not allowed to put'}, 400
        else:
            data = dict(parser.parse_args())
            data.pop('graph_id')  # 不应该允许修改graph_id
            update(node, data)
            db.session.add(node)
            db.session.commit()
            return node.id, 201

    def delete(self, nid):
        """
        file: swagger/node_delete.yml
        """
        node = Node.query.get(nid)
        if node is None:
            return {'msg': 'Invalid nid'}, 400
        db.session.delete(node)
        db.session.commit()
        return '', 204


class NodePicApi(Resource):

    method_decorators = [jwt_required]

    def put(self, nid):
        """
        file: swagger/node_pic_put.yml
        """
        current_uid = get_jwt_identity()
        node = Node.query.get(nid)
        if not node:
            return {'msg': 'Invalid args'}, 400
        if node.owner_id != current_uid:
            return {'msg': 'Not allowed'}, 400
        path = node.pic
        with open(path, 'wb') as fp:
            fp.write(request.get_data())
        return '', 201

    def delete(self, nid):
        """
        file: swagger/node_pic_delete.yml
        """
        current_uid = get_jwt_identity()
        node = Node.query.get(nid)
        if not node:
            return {'msg': 'Invalid args'}, 400
        if node.owner_id != current_uid:
            return {'msg': 'Not allowed'}, 400
        path = node.pic
        if not os.path.isfile(path):
            return {'msg': 'Upload Picture first'}, 400
        os.remove(path)
        return '', 204
