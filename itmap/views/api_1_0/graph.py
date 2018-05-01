# coding=utf-8

from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
)

from itmap.ext import db
from itmap.models.graph import Graph
from itmap.utils import update


relation_fields = {
    'sid': fields.Integer(attribute='source_node_id'),
    'tid': fields.Integer(attribute='target_node_id'),
    'source': fields.String(attribute='from_node.name'),
    'target': fields.String(attribute='to_node.name'),
    'gid': fields.Integer(attribute='graph_id'),
    'timestamp': fields.DateTime,
    'info': fields.String,
    'color': fields.String,
    'is_dual_way': fields.Boolean,
    'line_type': fields.String,
}


class FromNodeField(fields.Raw):
    def format(self, value):
        nodes = value.all()
        return [n.source_node_id for n in nodes]


class ToNodeField(fields.Raw):
    def format(self, value):
        nodes = value.all()
        return [n.target_node_id for n in nodes]


node_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'relate_page_url': fields.String,
    'is_template': fields.Boolean,
    'color': fields.String,
    'size': fields.String,
    'shape': fields.String,
    'gid': fields.Integer,
    'from_nodes': FromNodeField,
    'to_nodes': ToNodeField,
}

graph_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'owner_id': fields.Integer,
    'nodes': fields.List(fields.Nested(node_fields)),
    'relations': fields.List(fields.Nested(relation_fields)),
}


parser = reqparse.RequestParser()
parser.add_argument('name', trim=True)
parser.add_argument('graph_type')
parser.add_argument('is_private', type=bool)


class GraphListApi(Resource):

    method_decorators = [jwt_required]

    def get(self, uid):
        current_uid = get_jwt_identity()
        if uid == current_uid:
            graphs = Graph.query.filter_by(owner_id=uid).all()
        else:
            graphs = Graph.query.filter_by(owner_id=uid, is_private=False).all()
        return [{'id': g.id, 'name': g.name, 'owner_id': g.owner_id} for g in graphs]

    def post(self, uid):
        current_uid = get_jwt_identity()
        if uid != current_uid:
            return {'msg': 'Not Allowed to post'}, 400
        vals = dict(parser.parse_args())
        vals.update({
            'owner_id': uid,
        })
        graph = Graph(**vals)
        db.session.add(graph)
        db.session.commit()
        return graph.id, 201


class GraphApi(Resource):

    method_decorators = [jwt_required]

    @marshal_with(graph_fields)
    def get(self, gid):
        graph = Graph.query.get(gid)
        if graph is None:
            return {'msg': 'Invalid gid'}, 400
        return graph

    def delete(self, gid):
        graph = Graph.query.get(gid)
        if graph is None:
            return {'msg': 'Invalid gid'}, 400
        db.session.delete(graph)
        db.session.commit()
        return '', 204

    def put(self, gid):
        graph = Graph.query.get(gid)
        uid = get_jwt_identity()
        if graph is None:
            return {'msg': 'Invalid gid'}, 400
        elif graph.owner_id != uid:
            return {'msg': 'Not allowed to put'}, 400
        else:
            update(graph, dict(parser.parse_args()))
            db.session.add(graph)
            db.session.commit()
            return graph.id, 201
