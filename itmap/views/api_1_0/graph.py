# coding=utf-8

from collections import OrderedDict

from flask import request
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
)

from itmap.ext import db
from itmap.models.graph import Graph


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


class GraphListApi(Resource):

    @jwt_required
    def get(self):
        uid = get_jwt_identity()
        graphs = Graph.query.filter_by(owner_id=uid).all()
        return [{'id': g.id, 'name': g.name, 'owner_id': g.owner_id} for g in graphs]

    @jwt_required
    def post(self):
        uid = get_jwt_identity()
        data = request.json
        data = dict(data)
        graph = Graph(name=data['name'], owner_id=uid)
        db.session.add(graph)
        db.session.commit()
        return graph.id, 200


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
        return '', 200

    def put(self, gid):
        graph = Graph.query.get(gid)
        uid = get_jwt_identity()
        name = request.form['name']
        if graph is None:
            graph = Graph(name=name, owner_id=uid)
        elif graph.owner_id != uid:
            return {'msg': 'Not allowed to put'}, 400
        else:
            graph.name = name
        db.session.add(graph)
        db.session.commit()
        return graph.id, 200
