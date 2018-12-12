from datetime import datetime

from itmap.ext import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=True)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(2048))

    def __repr__(self):
        return '<Comment {!r}>'.format(self.title)
