# coding=utf-8

from datetime import datetime
from sqlalchemy import or_
from itmap.ext import db


class NodeRelation(db.Model):
    __tablename__ = 'node_relations'

    source_node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), primary_key=True)
    target_node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), primary_key=True)
    graph_id = db.Column(db.Integer, db.ForeignKey('graphs.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    info = db.Column(db.String(255), default='')
    color = db.Column(db.String(255))
    is_dual_way = db.Column(db.Boolean, default=False)  # 是双向还是单向
    line_type = db.Column(db.String(255))  # 线的类型
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    def __repr__(self):
        arch = '<->' if self.is_dual_way else '->'
        return '<NodeRelation {!r}{}{!r}>'.format(self.from_node.name, arch, self.to_node.name)

    @classmethod
    def find_relation(cls, sid, tid, gid, oid=None):
        kwargs = {
            'source_node_id': sid,
            'target_node_id': tid,
            'graph_id': gid,
        }
        if oid is not None:
            kwargs.update({'owner_id': oid})
        rels = cls.query.filter_by(**kwargs).first()
        return rels

    @classmethod
    def get_relation_by_node_id(cls, nid):
        return cls.query.filter(or_(cls.source_node_id == nid, cls.target_node_id == nid)).all()


class Node(db.Model):
    __tablename__ = 'nodes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=True)
    relate_page_url = db.Column(db.String(128))

    is_template = db.Column(db.Boolean, default=False)  # 是否作为模板

    color = db.Column(db.String(255))
    size = db.Column(db.String(255))  # 大小
    shape = db.Column(db.String(255))  # 形状
    description = db.Column(db.String(255))

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    graph_id = db.Column(db.Integer, db.ForeignKey('graphs.id'))
    from_nodes = db.relationship('NodeRelation',
                                  foreign_keys=[NodeRelation.target_node_id],
                                  backref=db.backref('to_node', lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')
    to_nodes = db.relationship('NodeRelation',
                                foreign_keys=[NodeRelation.source_node_id],
                                backref=db.backref('from_node', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    def __repr__(self):
        return '{}'.format(self.name)

    @property
    def pic(self):
        return '{}.jpg'.format(self.id)


class Graph(db.Model):
    __tablename__ = 'graphs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    graph_type = db.Column(db.String(64))
    is_private = db.Column(db.Boolean, default=False)  # 是否仅自己可见

    nodes = db.relationship('Node', backref='graph', cascade='all, delete-orphan')
    relations = db.relationship('NodeRelation', backref='graph', cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    def __repr__(self):
        return '{}'.format(self.name)
