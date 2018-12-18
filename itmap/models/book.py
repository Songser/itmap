from datetime import datetime

from itmap.ext import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    url = db.Column(db.String(256))
    author = db.Column(db.String(64))
    source = db.Column(db.String(32))
    description = db.Column(db.String(2048))
    image = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)