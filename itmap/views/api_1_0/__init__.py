# coding=utf-8

from flask import Blueprint
from flask_restful import Api

from .graph import GraphListApi, GraphApi, GraphFashionApi
from .node import NodeApi, NodePostApi
from .relation import NodeRelationApi
from .user import UserApi

bp = Blueprint('api', __name__, url_prefix='/api/v1_0')
api = Api(bp)
api.add_resource(GraphListApi, '/users/<int:uid>/graphs')
api.add_resource(GraphApi, '/graphs/<int:gid>')
api.add_resource(GraphFashionApi, '/graphs/fashion')
api.add_resource(NodeApi, '/nodes/<int:nid>')
api.add_resource(NodePostApi, '/nodes')
api.add_resource(NodeRelationApi, '/node_rels')
api.add_resource(UserApi, '/users/<int:uid>')
