# coding=utf-8

from flask import Blueprint
from flask_restful import Api

from .graph import GraphListApi, GraphApi, \
 NodeApi, NodeRelationApi, GraphNodeRelationApi
from .user import UserApi

bp = Blueprint('api', __name__, url_prefix='/api/v1_0')
api = Api(bp)
api.add_resource(GraphListApi, '/graphs')
api.add_resource(GraphApi, '/graph/<int:gid>')
api.add_resource(NodeApi, '/node/<int:nid>')
api.add_resource(NodeRelationApi, '/node_rel')
api.add_resource(UserApi, '/user/<int:uid>')
api.add_resource(GraphNodeRelationApi, '/graphs/<int:gid>/nodes')