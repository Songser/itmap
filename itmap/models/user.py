# coding=utf-8

#import arrow
from datetime import datetime
from flask import url_for, current_app
from flask_mail import Message
from flask_security import UserMixin, RoleMixin, AnonymousUser
import hashlib
from werkzeug import security

from itmap.ext import db, redis, mail, login_manager


class Permission(object):
    OPERATE_MAPS = 0x01
    OPERATE_RESOURCE = 0x02
    OPERATE_QUESTION = 0x04
    DELETE = 0x08
    ADMINISTER = 0x80


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    default = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(80), unique=True, index=True, nullable=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role')

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

    def __repr__(self):
        return '<Role {!r}'.format(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=True)
    nickname = db.Column(db.String(80), unique=True, index=True, nullable=True)
    password = db.Column(db.String(255))

    #mobile = db.Column()
    email = db.Column(db.String(120), unique=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    write_time = db.Column(db.DateTime)

    current_sign_in_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_sign_in_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {!r}>'.format(self.name)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email in current_app.config['ITMAP_ADMINS']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            else:
                self.role = Role.qeury.filter_by(default=True).first()

    @property
    def url(self):
        return url_for('user.detail', id=str(self.id))

    @property
    def email_md5(self):
        email = self.email.strip()
        if isinstance(email, str):
            email = email.encode('utf-8')
        return hashlib.md5(email).hexdigest()

    def avatar(self):
        return '{}{}.jpg'.format(current_app.config['AVATAR_BASE_URL'], self.email_md5)

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

    def set_password(self, password):
        self.password = self.generate_password(password)

    def check_password(self, password):
        return security.check_password_hash(
            self.password,
            current_app.config['SECRET_KEY'] + password
        )

    def reset_password(self):
        key = self.name + 'token'
        redis.set(key, self.create_token())
        redis.expire(key, 3600)
        msg = Message('Reset password',
                      sender=current_app.config['MAIL_SENDER'],
                      recipients=[self.email])
        msg.body = 'link to check token callback'
        mail.send(msg)

    def change_password(self, password, token):
        key = self.name + 'token'
        if token != redis.get(key):
            return False, 'token expired or wrong'
        new_password = self.generate_password(password)
        if self.password == new_password:
            return False, 'duplicate password'
        else:
            self.password = new_password
            db.session.add(self)
            db.session.commit()
            redis.remove(key)
            return True, 'success'

    @classmethod
    def by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


class AnonymousUser(AnonymousUser):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser
