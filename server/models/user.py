# coding=utf-8

import arrow
import logging

from datetime import datetime
import hashlib
from threading import Thread
from werkzeug import security

from flask import url_for, current_app, abort
from flask_admin.contrib import sqla
from flask_mail import Message
from flask_security import (
    UserMixin,
    RoleMixin,
    AnonymousUser,
    current_user,
)

from itmap.ext import db, redis, login_manager, mail
from itmap.utils import send_async_email

logger = logging.getLogger(__name__)

class Permission(object):
    OPERATE_MAPS = 0x01
    OPERATE_RESOURCE = 0x02
    OPERATE_QUESTION = 0x04
    DELETE = 0x08
    ADMINISTER = 0x80

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    default = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(80), unique=True, index=True, nullable=True)
    permissions = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.OPERATE_MAPS |
                     Permission.OPERATE_QUESTION |
                     Permission.OPERATE_RESOURCE, True),
            'Administrator': (0xff, False),
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
        else:  # then
            db.session.commit()
    
    @staticmethod
    def get(name):
        return Role.query.filter_by(name=name).first()

    def __repr__(self):
        return '<Role {!r}>'.format(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(32))
    gender = db.Column(db.String(8))
    birthday = db.Column(db.Date)

    email = db.Column(db.String(120), unique=True)
    has_verified = db.Column(db.Boolean, default=False)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    own_graphs = db.relationship('Graph', backref='owner')

    active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    write_time = db.Column(db.DateTime)

    current_sign_in_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_sign_in_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    def __repr__(self):
        return '<User {!r}>'.format(self.name or self.email)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # if self.role is None:
        #     if self.email in current_app.config['ITMAP_ADMINS']:
        #         self.role = Role.query.filter_by(permissions=0xff).first()
        #     else:
        #         self.role = Role.query.filter_by(default=True).first()

    @property
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'has_verified': self.has_verified,
            # 'role': self.role.name,
            'active': self.active,
            # 'current_sign_in_time': arrow.get(self.current_sign_in_time).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss'),
            # 'last_sign_in_time': arrow.get(self.last_sign_in_time).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss'),
            # 'own_graphs': [{'id':g.id, 'name':g.name, 'owner_id': self.id} for g in self.own_graphs],
            'avatar': self.avatar,
            'phone': self.phone,
            'gender': self.gender,
        }

    #@property
    #def url(self):
    #    return url_for('user.detail', id=str(self.id))

    @property
    def email_md5(self):
        email = self.email.strip()
        if isinstance(email, str):
            email = email.encode('utf-8')
        return hashlib.md5(email).hexdigest()

    @property
    def avatar(self):
        return '{}.jpg'.format(self.email_md5)

    @staticmethod
    def get(id):
        return User.query.get(id)

    @staticmethod
    def generate_password(password):
        return security.generate_password_hash(
            current_app.config['SECRET_KEY'] + password
        )

    @staticmethod
    def create_token(length=16):
        return security.gen_salt(length)

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        password = cls.generate_password(password)
        user = cls(name=username, password=password, email=email, **kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    def set_password(self, password):
        self.password = self.generate_password(password)

    def check_password(self, password):
        return security.check_password_hash(
            self.password,
            current_app.config['SECRET_KEY'] + password
        )

    def reset_password(self):
        if not self.has_verified:
            return False, 'Should verify first'
        key = self.name + 'change_password_token'
        token = self.create_token()
        redis.set(key, token)
        redis.expire(key, 3600)
        msg = Message(subject=u'重设密码',
                      body='http://127.0.0.1:5000/auth/change_password?token={}'.format(token),  # need modify
                      recipients=[self.email])
        # thread = Thread(target=send_async_email, args=[current_app, msg])
        # thread.start()
        # 虽然很多地方都给出了以上的用法，但这种方法会报错：RuntimeError: Working outside of application context.
        # 大概原因是current_app是线程的本地对象，不能传给别的线程？
        mail.send(msg)
        return True, 'Success'

    def change_password(self, password, token):
        key = self.name + 'change_password_token'
        if token != redis.get(key):
            return False, 'Token expired or wrong'
        new_password = self.generate_password(password)
        if self.password == new_password:
            return False, 'Duplicate password'
        else:
            self.password = new_password
            db.session.add(self)
            db.session.commit()
            redis.remove(key)
            return True, 'Success'

    def send_verify_email(self):
        if self.has_verified:
            return False, 'Already verified'
        key = self.name + self.email + 'verify_email_token'
        token = self.create_token()
        redis.set(key, token)
        redis.expire(key, 3600)
        msg = Message(subject=u'验证邮箱',
                      body='http://www.songcser.com/auth/verified_by_email?token={}'.format(token),  # need modify
                      recipients=[self.email])
        # thread = Thread(target=send_async_email, args=[current_app, msg])
        # thread.start()
        mail.send(msg)
        return True, 'Success'

    def verified_by_email(self, token):
        key = self.name + self.email + 'verify_email_token'
        if token != redis.get(key):
            return False, 'Token expired or wrong'
        self.has_verified = True
        db.session.add(self)
        db.session.commit()
        redis.remove(key)
        return True, 'Success'

    @classmethod
    def by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # def can(self, permissions):
    #     return self.role is not None and \
    #         (self.role.permissions & permissions) == permissions

    # def is_administrator(self):
    #     return self.can(Permission.ADMINISTER)

    def sign_stamp(self):
        self.last_sign_in_time = self.current_sign_in_time
        self.current_sign_in_time = datetime.utcnow()
        db.session.add(self)
        db.session.commit()


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


class AnonymousUser(AnonymousUser):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('Administrator')
        )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
