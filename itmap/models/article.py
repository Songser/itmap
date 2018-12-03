from datetime import datetime

from itmap.ext import db


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=True)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    url = db.Column(db.String(128))
    author = db.Column(db.String(64))
    source = db.Column(db.String(32))
    description = db.Column(db.String(2048))
    body = db.Column(db.Text())

    def __repr__(self):
        return '<Article {!r}>'.format(self.title)
