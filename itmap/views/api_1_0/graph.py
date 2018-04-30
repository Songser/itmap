# coding=utf-8

from collections import OrderedDict

from flask import request
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
)

from itmap.ext import db
from itmap.models.graph import NodeRelation, Node, Graph
from itmap.utils import update


relation_fields = {
    'sid': fields.Integer(attribute='source_node_id'),
    'tid': fields.Integer(attribute='target_node_id'),
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


class NodeRelationApi(Resource):

    method_decorators = [jwt_required]

    def put(self):
        data = request.json
        data = dict(data)
        sid = data.get('source_node_id')
        tid = data.get('target_node_id')
        gid = data.get('graph_id')
        if not (sid and tid and gid):
            return {'msg': 'Invalid args'}, 400
        relation = NodeRelation.find_relation(sid, tid, gid)
        uid = get_jwt_identity()
        if relation is None:
            data.update({
                'owner_id': uid,
            })
            relation = NodeRelation(**data)
        elif relation.owner_id != uid:
            return {'msg': 'Not allowed to put'}, 400
        else:
            update(relation, data)
        db.session.add(relation)
        db.session.commit()
        return '', 200

    def delete(self):
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
        return '', 200

class GraphNodeRelationApi(Resource):

    def get(self, gid):
        graph = Graph.query.get(gid)
        nodes = Node.query.filter_by(graph_id=gid).all()
        relations = NodeRelation.query.filter_by(graph_id=gid).all()
        nodes = [{"name": node.name} for node in nodes]
        links = [{
            "source": Node.query.get(rel.source_node_id).name,
            "target": Node.query.get(rel.target_node_id).name, 
            } for rel in relations]
        return {'nodes': nodes, 'links': links}