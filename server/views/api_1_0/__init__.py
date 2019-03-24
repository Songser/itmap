# coding=utf-8

from flask import Blueprint
from flask_restful import Api

from .graph import GraphListApi, GraphApi, GraphFashionApi
from .node import NodeApi, NodePostApi, NodePicApi
from .relation import NodeRelationApi
from .user import UserApi, UserAvatarApi
from .article import ArticleListApi
from .comment import CommentListApi
from .book import BookListApi, BookPicApi
from .errors import errors

bp = Blueprint('api', __name__, url_prefix='/api/v1_0')
api = Api(bp, errors=errors)
api.add_resource(GraphListApi, '/users/<int:uid>/graphs')
api.add_resource(GraphApi, '/graphs/<int:gid>')
api.add_resource(GraphFashionApi, '/graphs/fashion')
api.add_resource(NodeApi, '/nodes/<int:nid>')
api.add_resource(NodePostApi, '/nodes')
api.add_resource(NodePicApi, '/nodes/<int:nid>/pic')
api.add_resource(NodeRelationApi, '/node_rels')
api.add_resource(UserApi, '/users/<int:uid>')
api.add_resource(UserAvatarApi, '/users/<int:uid>/avatar')
api.add_resource(ArticleListApi, '/nodes/<int:nid>/articles')
api.add_resource(CommentListApi, '/nodes/<int:nid>/comments')
api.add_resource(BookListApi, '/nodes/<int:nid>/books')
api.add_resource(BookPicApi, '/books/<int:bid>/pic')