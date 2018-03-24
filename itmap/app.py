# coding=utf-8

from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return '<h1>Hello World</h1>', 200


if __name__ == '__main__':
    app.run(debug=True)
