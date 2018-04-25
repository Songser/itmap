# coding=utf-8

from datetime import datetime

from itmap.ext import db


class NodeRelation(db.Model):
    __tablename__ = 'node_relations'

    source_node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), primary_key=True)
    target_node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), primary_key=True)
    graph_id = db.Column(db.Integer, db.ForeignKey('graphs.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    info = db.Column(db.String(255))
    color = db.Column(db.String(255))
    is_dual_way = db.Column(db.Boolean, default=False)  # 是双向还是单向
    line_type = db.Column(db.String(255))  # 线的类型

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


class Node(db.Model):
    __tablename__ = 'nodes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=True)
    relate_page_url = db.Column(db.String(64))

    is_template = db.Column(db.Boolean, default=False)  # 是否作为模板

    color = db.Column(db.String(255))
    size = db.Column(db.String(255))  # 大小
    shape = db.Column(db.String(255))  # 形状

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

    def __repr__(self):
        return '<Node {!r}>'.format(self.name)


class Graph(db.Model):
    __tablename__ = 'graphs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    nodes = db.relationship('Node', backref='graph')
    relations = db.relationship('NodeRelation', backref='graph')

    def __repr__(self):
        return '<Graph {!r}>'.format(self.name)

    def remove(self):
        db.session.delete(self.relations)
        db.session.delete(self.nodes)
        db.session.delete(self)
        db.session.commit()
