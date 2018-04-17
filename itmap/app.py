# coding=utf-8

import click
import code
import sys
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
    click.echo('{}'.format(sys.path))


try:
    import IPython
    has_ipython = True
except ImportError:
    has_ipython = False


def plain_shell(user_ns, banner):
    sys.exit(code.interact(banner=banner, local=user_ns))


def ipython_shell(user_ns, banner):
    IPython.embed(banner1=banner, user_ns=user_ns)


@app.cli.command('ipython', short_help='Runs a shell in the app context.', with_appcontext=True)
@click.option('--plain', help='Use Plain Shell', is_flag=True)
def shell_command(plain):
    from flask.globals import _app_ctx_stack
    app = _app_ctx_stack.top.app
    banner = 'Python %s on %s\nApp: %s%s\nInstance: %s' % (
        sys.version,
        sys.platform,
        app.import_name,
        app.debug and ' [debug]' or '',
        app.instance_path,
    )
    user_ns = app.make_shell_context()
    use_plain_shell = not has_ipython or plain
    if use_plain_shell:
        plain_shell(user_ns, banner)
    else:
        ipython_shell(user_ns, banner)


@app.route('/', methods=['GET'])
def index():
    return '<h1>Hello World</h1>', 200
