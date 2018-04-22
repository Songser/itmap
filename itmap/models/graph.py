# coding=utf-8

from datetime import datetime
from flask import url_for, current_app

from itmap.ext import db


class GraphRelation(db.Model):
    __tablename__ = 'graph_relations'

    source_graph_id = db.Column(db.Integer, db.ForeignKey('graphs.id'),
                                primary_key=True)
    target_graph_id = db.Column(db.Integer, db.ForeignKey('graphs.id'),
                                primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    info = db.Column(db.String(255))
    color = db.Column(db.String(255))
    is_dual_way = db.Column(db.Boolean, default=False)  # 是双向还是单向
    line_type = db.Column(db.String(255))  # 线的类型


class Graph(db.Model):
    __tablename__ = 'graphs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    relate_page_url = db.Column(db.String(64))

    from_graphs = db.relationship('GraphRelation',
                                  foreign_keys=[GraphRelation.target_graph_id],
                                  backref=db.backref('to_graph', lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')
    to_graphs = db.relationship('GraphRelation',
                                foreign_keys=[GraphRelation.source_graph_id],
                                backref=db.backref('from_graph', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    color = db.Column(db.String(255))
    size = db.Column(db.String(255))  # 大小
    shape = db.Column(db.String(255))  # 形状



