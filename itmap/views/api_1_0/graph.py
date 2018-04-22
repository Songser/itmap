# coding=utf-8

from collections import OrderedDict
from flask_restful import Resource, fields, marshal, marshal_with, reqparse

from itmap.models.graph import GraphRelation, Graph


graph_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'user_id': fields.Integer,
    'relate_page_url': fields.String,
    'color': fields.String,
    'size': fields.String,
    'shape': fields.String,
}


graphlist_parser = reqparse.RequestParser()
graphlist_parser.add_argument('ids', type=tuple)


class GraphListApi(Resource):
    def get(self):
        args = graphlist_parser.parse_args()
        gids = args['ids']
        graphs = Graph.query.filter_by(id in gids).all()
        return OrderedDict(
            {'graphs': marshal(graphs, graph_fields)}
        )


graph_parser = reqparse.RequestParser()
graph_parser.add_argument('id', type=int)


class GraphApi(Resource):
    @marshal_with(graph_fields)
    def get(self):
        args = graph_parser.parse_args()
        gid = args['id']
        graph = Graph.query.filter_by(id=gid).first()
        return graph

    def put(self):
        pass


class GraphRelationApi(Resource):
    def get(self):
        pass

    def put(self):
        pass
