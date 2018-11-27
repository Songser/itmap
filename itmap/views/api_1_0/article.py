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

from itmap.models.article import Article

aritcle_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'node_id': fields.Integer,
    'url': fields.String,
    'author': fields.String,
    'source': fields.String,
    'description': fields.String,
}

class ArticleListApi(Resource):

    def get(self, nid):
        articles = Article.query.filter_by(node_id=nid) \
            .order_by(Article.id).all()
        return [
            marshal(a, aritcle_fields)
            for a in articles
        ]