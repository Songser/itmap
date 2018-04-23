# coding=utf-8

from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login')
def login():
    pass


@bp.route('/register', method=['POST'])
def register():
    pass


@bp.route('/logout')
def logout():
    pass
