from flask import Flask

from logging.config import dictConfig

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

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return (
        '<h1>Hello World!</h1>'
        '<strong>My first site!</strong>'
    )

@app.route('/users')
def users():
    app.logger.info("GET users!")
    print("GET users print!")
    return [{'name': "Vitalii", 'age': 35}, {'name': "Olia", 'age': 25}]

@app.route('/debug')
def debug():
    message ="asdasd"
    return message

if __name__ == '__main__':
    app.run(debug=True)