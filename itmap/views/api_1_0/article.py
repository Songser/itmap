from flask import request
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
from itmap.models.graph import Node
from itmap.ext import db

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('title', trim=True)
parser.add_argument('url')
parser.add_argument('author')
parser.add_argument('source')
parser.add_argument('description')

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
        limit = 20
        page = int(request.args.get('page', 0))
        articles = Article.query.filter_by(node_id=nid) \
            .order_by(Article.id)\
            .offset(page * limit)\
            .limit(limit)\
            .all()
        return [
            marshal(a, aritcle_fields)
            for a in articles
        ]

    @jwt_required
    def post(self, nid):
        node = Node.query.get(nid)
        if node is None:
            return {'msg': 'Invalid nid'}, 400
        uid = get_jwt_identity()
        vals = dict(parser.parse_args())
        vals.update({
            'owner_id': uid,
            'node_id': nid,
        })
        article = Article(**vals)
        db.session.add(article)
        db.session.commit()
        return article.id, 201
