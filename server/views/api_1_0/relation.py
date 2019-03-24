# coding=utf-8

from collections import OrderedDict

from flask import request
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
)

from itmap.ext import db
from itmap.models.graph import NodeRelation, Node
from itmap.utils import update


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('source_node_id', type=int, required=True)
parser.add_argument('target_node_id', type=int, required=True)
parser.add_argument('graph_id', type=int, required=True)
parser.add_argument('info')
parser.add_argument('color', choices=('red', 'green', 'yellow', 'blue'), help='Bad choice: {error_msg}')
parser.add_argument('is_dual_way', type=bool)
parser.add_argument('line_type', choices=('bold', 'dotted', 'common'), help='Bad choice: {error_msg}')


class NodeRelationApi(Resource):

    method_decorators = [jwt_required]

    def post(self):
        """
        file: swagger/relation_post.yml
        """
        uid = get_jwt_identity()
        vals = dict(parser.parse_args())
        source = Node.query.get(vals['source_node_id'])
        target = Node.query.get(vals['target_node_id'])
        if not (source and target
                and source.graph_id == vals['graph_id']
                and source.graph_id == target.graph_id
                and source.owner_id == uid
                and target.owner_id == uid):
            return {'msg': 'Invalid args'}, 400
        relation = NodeRelation.find_relation(source.id, target.id, source.graph_id)
        if relation:
            return {'msg': 'Already exists'}, 400
        vals.update({
            'owner_id': uid,
        })
        relation = NodeRelation(**vals)
        db.session.add(relation)
        db.session.commit()
        return True, 201

    def put(self):
        """
        file: swagger/relation_put.yml
        """
        vals = dict(parser.parse_args())
        sid = vals.pop('source_node_id')
        tid = vals.pop('target_node_id')
        gid = vals.pop('graph_id')
        relation = NodeRelation.find_relation(sid, tid, gid)
        uid = get_jwt_identity()
        if not (relation and relation.owner_id == uid):
            return {'msg': 'Not allowed to put'}, 400
        else:
            update(relation, vals)
        db.session.add(relation)
        db.session.commit()
        return '', 201

    def delete(self):
        """
        file: swagger/relation_delete.yml
        """
        data = request.json
        data = dict(data)
        sid = data.get('source_node_id')
        tid = data.get('target_node_id')
        gid = data.get('graph_id')
        if not (sid and tid and gid):
            return {'msg': 'Invalid args'}, 400
        relation = NodeRelation.find_relation(sid, tid, gid)
        if relation is None:
            return {'msg': 'Invalid args'}, 400
        db.session.delete(relation)
        db.session.commit()
        return '', 204
