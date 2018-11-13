# coding=utf-8

from flask_restful import (
    Resource,
    fields,
    marshal_with,
    reqparse,
    marshal,
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    jwt_optional,
)

from itmap.ext import db, redis
from itmap.models.graph import Graph
from itmap.utils import update


relation_fields = {
    'sid': fields.Integer(attribute='source_node_id'),
    'tid': fields.Integer(attribute='target_node_id'),
    'source': fields.String(attribute='from_node.name'),
    'target': fields.String(attribute='to_node.name'),
    'gid': fields.Integer(attribute='graph_id'),
    'timestamp': fields.DateTime,
    'value': fields.String(attribute='info'),
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
    'description': fields.String,
    'gid': fields.Integer,
    'from_nodes': FromNodeField,
    'to_nodes': ToNodeField,
    'pic': fields.String,
}

graph_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'owner_id': fields.Integer,
    'owner_name': fields.String(attribute='owner.name'),
    'nodes': fields.List(fields.Nested(node_fields)),
    'relations': fields.List(fields.Nested(relation_fields)),
}


parser = reqparse.RequestParser()
parser.add_argument('name', trim=True)
#parser.add_argument('graph_type')
parser.add_argument('is_private', type=bool)


class GraphListApi(Resource):

    method_decorators = [jwt_required]

    def get(self, uid):
        """
        file: swagger/graph_list_get.yml
        """
        current_uid = get_jwt_identity()
        if uid == current_uid:
            graphs = Graph.query.filter_by(owner_id=uid).order_by(Graph.id).all()
        else:
            graphs = Graph.query.filter_by(owner_id=uid, is_private=False).order_by(Graph.id).all()
        return [{'id': g.id, 'name': g.name, 'owner_id': g.owner_id} for g in graphs]

    def post(self, uid):
        """
        file: swagger/graph_post.yml
        """
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


class GraphFashionApi(Resource):

    def get(self):
        """
        file: swagger/graph_fashion_get.yml
        """
        gids = redis.smembers('graphs_fashion')
        if gids:
            gids = [int(item) for item in gids]
            graphs = Graph.query.filter(Graph.id.in_(gids)).all()
        else:
            graphs = Graph.query.filter_by(graph_type='fashion').all()
            [redis.sadd('graphs_fashion', graph.id) for graph in graphs]
            redis.expire('graphs_fashion', 600)
        return [{'id': g.id, 'name': g.name, 'owner_id': g.owner_id} for g in graphs]


class GraphApi(Resource):

    # method_decorators = [jwt_required]

    #@marshal_with(graph_fields)
    def get(self, gid):
        """
        file: swagger/graph_get.yml
        """
        graph = Graph.query.get(gid)
        if graph is None:
            return {'msg': 'Invalid gid'}, 400
        if graph.graph_type != 'fashion':
            uid = get_jwt_identity()
            if not uid:
                return {'msg': 'Not allowed'}, 401
        raw_result = marshal(graph, graph_fields)
        raw_result['nodes'].sort(key=lambda r: r['id'])
        raw_result['relations'].sort(key=lambda r: r['sid'])
        return raw_result

    @jwt_required
    def delete(self, gid):
        """
        file: swagger/graph_delete.yml
        """
        graph = Graph.query.get(gid)
        if graph is None:
            return {'msg': 'Invalid gid'}, 400
        db.session.delete(graph)
        db.session.commit()
        return '', 204

    @jwt_required
    def put(self, gid):
        """
        file: swagger/graph_put.yml
        """
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
