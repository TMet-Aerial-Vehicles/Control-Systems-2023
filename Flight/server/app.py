from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return "CS-Flight Flask Server"


@app.route('/testing', methods=['GET'])
def testing():
    return {"body": "Hello World! - Flight"}


if __name__ == '__main__':
    app.run()
