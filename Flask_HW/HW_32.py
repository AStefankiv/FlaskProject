from flask import Flask, jsonify
from logging.config import dictConfig

app = Flask(__name__)

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

@app.route('/')
def hello_world():
    return (
        '<h1>Hello Visitor!</h1>'
        '<br><a href="/hello">/hello</a><br>'
        '<br><a href="/html">/html</a><br>'
        '<br><a href="/json">/json</a><br>'
    )

@app.route('/hello', methods=['GET'])
def hello():
    app.logger.info('Hello endpoint-log')
    return 'Hello, world!'

@app.route('/html', methods=['GET'])
def html():
    app.logger.info('HTML endpoint-log')
    return (
            '<h1>Hello, HTML!</h1>'
            '<h1>Good morning, teacher Vitalii</h1>'
    )

@app.route('/json', methods=['GET'])
def json():
    app.logger.info('JSON endpoint-log')
    data = {'message': 'Good afternoon, Hrebennikov!'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)