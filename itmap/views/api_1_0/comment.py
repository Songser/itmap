from flask import request
from flask_restful import (
    Resource,
    fields,
    reqparse,
    marshal,
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from itmap.models.comment import Comment
from itmap.models.graph import Node
from itmap.ext import db

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('title', trim=True)
parser.add_argument('description')

comment_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'node_id': fields.Integer,
    'description': fields.String,
}

class CommentListApi(Resource):

    def get(self, nid):
        limit = 20
        page = int(request.args.get('page', 0))
        comments = Comment.query.filter_by(node_id=nid) \
            .order_by(Comment.id)\
            .offset(page * limit)\
            .limit(limit)\
            .all()
        return [
            marshal(a, comment_fields)
            for a in comments
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
        comment = Comment(**vals)
        db.session.add(comment)
        db.session.commit()
        return comment.id, 201
