# coding=utf-8

from flask import Flask
from .ext import db, mail, redis, login_manager
import .config as _config


#@app.route('/', methods=['GET'])
#def index():
#    return '<h1>Hello World</h1>', 200

def create_app():
    app = Flask(__name__)
    app.config.from_object(_config)

    ####

    db.init_app(app)
    mail.init_app(app)
    redis.init_app(app)
    login_manager.init_app(app)

    return app

#if __name__ == '__main__':
#    app.run(debug=True)