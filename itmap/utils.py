# coding=utf-8

from itmap.ext import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def update(instance, data):
    for key, value in data.items():
        if hasattr(instance, key) and value is not None:
            setattr(instance, key, value)
