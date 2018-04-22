# coding=utf-8

from flask import Blueprint
from flask_restful import Api

from .graph import GraphListApi, GraphApi, GraphRelationApi

bp = Blueprint('api', __name__, url_prefix='/api/v1_0')
api = Api(bp)
api.add_resource(GraphListApi, '/graphs')
api.add_resource(GraphApi, '/graph')
api.add_resource(GraphRelationApi, '/graph_rel/<id>')
