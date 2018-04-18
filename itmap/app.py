# coding=utf-8

from flask import Flask
from ext import mail, redis, login_manager, db
import config as _config



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


@app.route('/', methods=['GET'])
def index():
    return '<h1>Hello World</h1>', 200
#if __name__ == '__main__':
#    app.run(debug=True)
