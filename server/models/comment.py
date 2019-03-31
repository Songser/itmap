from datetime import datetime

from itmap.ext import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=True)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User',
        backref=db.backref('comments', lazy='dynamic'))
    description = db.Column(db.String(2048))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)


    def __repr__(self):
        return '{}'.format(self.title)

    def to_dict(self):
        return {
            'id': self.id,
            'node_id': self.node_id,
            'title': self.title,
            'owner_id': self.owner_id,
            'owner_name': self.owner.name,
            'description': self.description,
        }
