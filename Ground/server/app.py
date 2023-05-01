from flask import Flask, request
from flask_socketio import SocketIO
import configparser
import os
import sys
sys.path.append('../../')

from Shared.loggingHandler import setup_logging
from Ground.server.groundController import GroundController


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))

app = Flask(__name__)

setup_logging(config['Ground']['App_Name'])
groundController = GroundController(SocketIO(app))


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return "CS-Ground Flask Server"


@app.route('/testing', methods=['GET'])
def testing():
    return {"body": "Hello World! - Ground"}


@app.route('/task-1', methods=['GET'])
def task_1():
    return


@app.route('/task-2', methods=['GET'])
def task_2():
    return


@app.route('/process-qr', methods=['POST'])
def process_qr():
    # Accepts 2 form parameters, raw_qr_string and qr_type (enum)
    # Process raw_qr_string if it conforms to the expected format of qr_type
    # Saves QR formatted class
    json_response = request.get_json()
    return groundController.process_qr(json_response)


@app.route('/get_parsed_qr/<qr_type>', methods=['GET'])
def get_parsed_qr(qr_type):
    # Accepts qr_type
    # Checks if that qr is set in variable
    # Returns success and qr data if found
    return groundController.get_qr(qr_type)


@app.route('/get-telemetry', methods=['GET'])
def get_telemetry():
    return groundController.get_latest_telemetry()


@app.route('/set-telemetry', methods=['POST'])
def set_telemetry():
    # Access POST telemetry
    json_response = request.get_json()
    # Process data, and notify event subscribers
    return groundController.process_telemetry(json_response)


@app.route('/manual-command', methods=['POST'])
def manual_command():
    # Receives form data containing longitude, latitude, priority values
    # Will log command for now
    return


if __name__ == '__main__':
    app.run(
        host=config['Ground']['API_Local_IP'],
        port=int(config['Ground']['API_IP_PORT'])
    )
