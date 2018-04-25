# coding=utf-8
import logging
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import (
    jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, jwt_optional, get_raw_jwt,
    jwt_refresh_token_required, get_jti, fresh_jwt_required,
)

from itmap.ext import db, redis, jwt
from itmap.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = logging.getLogger(__name__)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'role': user.role.name}


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis.get(jti)
    if entry is None:
        return True
    return entry == 'true'


@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is None:
        return jsonify({"msg": "Missing username parameter"}), 400
    if password is None:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(name=username).first()
    if user is None:
        return jsonify({"msg": "Invalid username"}), 400

    if not user.check_password(password):
        return jsonify({"msg": "Invalid password"}), 400

    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)

    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)
    redis.set(access_jti, 'false', current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 1.2)
    redis.set(refresh_jti, 'false', current_app.config['JWT_REFRESH_TOKEN_EXPIRES'] * 1.2)

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@bp.route('/refresh_login', methods=['POST'])
def refresh_login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is None:
        return jsonify({"msg": "Missing username parameter"}), 400
    if password is None:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(name=username).first()
    if user is None:
        return jsonify({"msg": "Invalid username"}), 400

    if not user.check_password(password):
        return jsonify({"msg": "Invalid password"}), 400

    access_token = create_access_token(identity=user, fresh=True)
    access_jti = get_jti(encoded_token=access_token)
    redis.set(access_jti, 'false', current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 1.2)

    return jsonify(access_token=access_token), 200


@bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    email = request.json.get('email', None)

    if username is None:
        return jsonify({"msg": "Missing username parameter"}), 400
    if password is None:
        return jsonify({"msg": "Missing password parameter"}), 400
    if email is None:
        return jsonify({"msg": "Missing email parameter"}), 400

    user = User.query.filter_by(name=username).first()
    if user is not None:
        return jsonify({"msg": "Already exists username"}), 400
    user = User.create_user(username=username, email=email, password=password)

    return jsonify(username=username, password=password), 200


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    uid = get_jwt_identity()
    current_user = User.query.get(uid)
    access_token = create_access_token(identity=current_user, fresh=False)
    access_jti = get_jti(encoded_token=access_token)
    redis.set(access_jti, 'false', current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 1.2)
    return jsonify(access_token=access_token), 200


@bp.route('/access_revoke', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    redis.set(jti, 'true', current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 1.2)
    return jsonify({"msg": "Access token revoked"}), 200


@bp.route('/refresh_revoke', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    redis.set(jti, 'true', current_app.config['JWT_REFRESH_TOKEN_EXPIRES'] * 1.2)
    return jsonify({"msg": "Refresh token revoked"}), 200


@bp.route('/current_user', methods=['GET'])
@jwt_optional
def current_user():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(logged_in_as=current_user), 200
    else:
        return jsonify(logged_in_as='anonymous user'), 200


@bp.route('/modify_email', methods=['POST'])
@fresh_jwt_required
def modify_email():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    if email is None:
        return jsonify({"msg": "Missing email parameter"}), 400

    uid = get_jwt_identity()
    current_user = User.query.get(uid)
    current_user.email = email
    db.session.add(current_user)
    db.session.commit()
    return jsonify(user=current_user), 200


@bp.route('/reset_password', methods=['GET'])
@fresh_jwt_required
def reset_password():
    uid = get_jwt_identity()
    current_user = User.query.get(uid)
    result, msg = current_user.reset_password()
    status_code = 200 if result else 400
    return jsonify({"msg": msg}), status_code


@bp.route('/change_password', methods=['POST'])
@fresh_jwt_required
def change_password():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    token = request.json.get('token', None)
    password = request.json.get('password', None)
    if token is None:
        return jsonify({"msg": "Missing token parameter"}), 400
    if password is None:
        return jsonify({"msg": "Missing password parameter"}), 400

    uid = get_jwt_identity()
    current_user = User.query.get(uid)
    result, msg = current_user.change_password(password, token)
    status_code = 200 if result else 400
    return jsonify({"msg": msg}), status_code


@bp.route('/verify_email', methods=['GET'])
@fresh_jwt_required
def send_verify_email():
    uid = get_jwt_identity()
    current_user = User.query.get(uid)
    result, msg = current_user.send_verify_email()
    status_code = 200 if result else 400
    return jsonify({"msg": msg}), status_code


@bp.route('/verified', methods=['POST'])
@fresh_jwt_required
def verified_by_email():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    token = request.json.get('token', None)
    if token is None:
        return jsonify({"msg": "Missing token parameter"}), 400

    uid = get_jwt_identity()
    current_user = User.query.get(uid)
    result, msg = current_user.verified_by_email(token)
    status_code = 200 if result else 400
    return jsonify({"msg": msg}), status_code
