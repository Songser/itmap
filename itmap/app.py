# coding=utf-8

import sys
print(sys.path)
import click
from flask import Flask
from itmap.ext import db, mail, redis, login_manager
import itmap.config as _config


def create_app():
    app = Flask(__name__)
    app.config.from_object(_config)

    ####

    db.init_app(app)
    mail.init_app(app)
    redis.init_app(app)
    login_manager.init_app(app)

    return app


app = create_app()


@app.cli.command()
def initdb():
    click.echo('Init the db')


@app.cli.command()
def sys_path():
    import sys
    click.echo('{}'.format(sys.path))


@app.route('/', methods=['GET'])
def index():
    return '<h1>Hello World</h1>', 200
