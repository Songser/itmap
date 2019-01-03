from flask import request, current_app
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

from itmap.models.book import Book
from itmap.models.graph import Node
from itmap.ext import db

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', trim=True)
parser.add_argument('url')
parser.add_argument('author')
parser.add_argument('source')
parser.add_argument('description')

book_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'node_id': fields.Integer,
    'url': fields.String,
    'author': fields.String,
    'source': fields.String,
    'description': fields.String,
    'pic': fields.String,
    'owner_id': fields.Integer,
}


class BookListApi(Resource):

    def get(self, nid):
        limit = 20
        page = int(request.args.get('page', 0))
        books = Book.query.filter_by(node_id=nid) \
            .order_by(Book.id)\
            .offset(page * limit)\
            .limit(limit)\
            .all()
        return [
            marshal(b, book_fields)
            for b in books
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
        book = Book(**vals)
        db.session.add(book)
        db.session.commit()
        return book.id, 201

class BookPicApi(Resource):
    
    method_decorators = [jwt_required]

    def post(self, bid):
        """
        file: swagger/book_pic_put.yml
        """
        current_uid = get_jwt_identity()
        book = Book.query.get(bid)
        if not book:
            return {'msg': 'Invalid args'}, 400
        if book.owner_id != current_uid:
            return {'msg': 'Not allowed'}, 400
        path = current_app.config['ABSOLUTE_BOOK_PICTURE_DIR'] + book.pic
        f = request.files['book_pic']
        f.save(path)
        return '', 201
