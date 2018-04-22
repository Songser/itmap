# coding=utf-8

import click
import code
from redis import Redis
import sys
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import rediscli
from itmap.ext import db, mail, redis, login_manager
from itmap.models.user import Role, User
from itmap.models.graph import GraphRelation, Graph
import itmap.config as _config


def create_app():
    app = Flask(__name__)
    app.config.from_object(_config)

    ####
    db.init_app(app)
    mail.init_app(app)
    redis.init_app(app)
    login_manager.init_app(app)

    admin = Admin(app, name='itmap', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Role, db.session))

    admin.add_view(ModelView(GraphRelation, db.session))
    admin.add_view(ModelView(Graph, db.session))

    admin.add_view(rediscli.RedisCli(redis._redis_client))
    return app


app = create_app()


@app.cli.command(with_appcontext=True)
def initdb():
    click.echo('Init the db')
    from itmap.models.user import Role, User
    from itmap.models.graph import GraphRelation, Graph
    # 必须在调用db.create_all之前导入具体的Model
    # 原因是如User这种类是元类Model的实例（大体上是）
    # 当导入时，实际上是创建了User类
    # 在此过程中，会将User注册到db.metadata.tables中（具体怎么串起来的没找到）
    db.drop_all()
    db.create_all()
    Role.insert_roles()
    for index, email in enumerate(app.config['ITMAP_ADMINS']):
        User.create_user(email=email, password=app.config['ITMAP_ADMIN_PASSWORD'], username='admin{}'.format(index))
    db.session.commit()


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
    #from flask.globals import _app_ctx_stack
    #app = _app_ctx_stack.top.app
    user_ns = app.make_shell_context()
    user_ns.update({'db': db, 'redis': redis})
    banner = 'Python %s on %s\nApp: %s%s\nInstance: %s\nuser_ns: %s' % (
        sys.version,
        sys.platform,
        app.import_name,
        app.debug and ' [debug]' or '',
        app.instance_path,
        user_ns,
    )
    use_plain_shell = not has_ipython or plain
    if use_plain_shell:
        plain_shell(user_ns, banner)
    else:
        ipython_shell(user_ns, banner)


# from https://github.com/ei-grad/flask-shell-ipython/blob/master/flask_shell_ipython.py
@app.cli.command('ipython2', context_settings=dict(ignore_unknown_options=True), with_appcontext=True)
@click.argument('ipython_args', nargs=-1, type=click.UNPROCESSED)
def shell(ipython_args):
    """Runs a shell in the app context.
    Runs an interactive Python shell in the context of a given
    Flask application. The application will populate the default
    namespace of this shell according to it's configuration.
    This is useful for executing small snippets of management code
    without having to manually configuring the application.
    """
    import IPython
    from IPython.terminal.ipapp import load_default_config
    from traitlets.config.loader import Config
    from flask.globals import _app_ctx_stack

    app = _app_ctx_stack.top.app

    if 'IPYTHON_CONFIG' in app.config:
        config = Config(app.config['IPYTHON_CONFIG'])
    else:
        config = load_default_config()

    config.TerminalInteractiveShell.banner1 = '''Python %s on %s
IPython: %s
App: %s%s
Instance: %s''' % (sys.version,
                   sys.platform,
                   IPython.__version__,
                   app.import_name,
                   app.debug and ' [debug]' or '',
                   app.instance_path)

    IPython.start_ipython(
        argv=ipython_args,
        user_ns=app.make_shell_context(),
        config=config,
    )


@app.route('/', methods=['GET'])
def index():
    return '<h1>Hello World</h1>', 200
