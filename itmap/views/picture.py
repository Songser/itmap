# coding=utf-8

from flask import Blueprint, send_from_directory, current_app

bp = Blueprint('picture', __name__)


@bp.route('/avatars/<path:path>', methods=['GET'])
def send_avatar(path):
    return send_from_directory(current_app.config['AVATAR_DIR'], path)


@bp.route('/node_pics/<path:path>', methods=['GET'])
def send_node_pic(path):
    return send_from_directory(current_app.config['NODE_PICTURE_DIR'], path)

@bp.route('/book_pics/<path:path>', methods=['GET'])
def send_book_pic(path):
    return send_from_directory(current_app.config['BOOK_PICTURE_DIR'], path)
