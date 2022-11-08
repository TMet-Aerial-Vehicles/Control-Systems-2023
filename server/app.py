from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return "Hello World!"


@app.route('/testing', methods=['GET'])
def testing():
    return {"body": "Hello World!"}


if __name__ == '__main__':
    app.run()
