# coding=utf-8

from collections import OrderedDict

from flask import request
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
)

from itmap.ext import db
from itmap.models.graph import NodeRelation
from itmap.utils import update


class NodeRelationApi(Resource):

    method_decorators = [jwt_required]

    def put(self):
        data = request.json
        data = dict(data)
        sid = data.get('source_node_id')
        tid = data.get('target_node_id')
        gid = data.get('graph_id')
        if not (sid and tid and gid):
            return {'msg': 'Invalid args'}, 400
        relation = NodeRelation.find_relation(sid, tid, gid)
        uid = get_jwt_identity()
        if relation is None:
            data.update({
                'owner_id': uid,
            })
            relation = NodeRelation(**data)
        elif relation.owner_id != uid:
            return {'msg': 'Not allowed to put'}, 400
        else:
            update(relation, data)
        db.session.add(relation)
        db.session.commit()
        return '', 200

    def delete(self):
        data = request.json
        data = dict(data)
        sid = data.get('source_node_id')
        tid = data.get('target_node_id')
        gid = data.get('graph_id')
        if not (sid and tid and gid):
            return {'msg': 'Invalid args'}, 400
        relation = NodeRelation.find_relation(sid, tid, gid)
        if relation is None:
            return {'msg': 'Invalid args'}, 400
        db.session.delete(relation)
        db.session.commit()
        return '', 200
