from flask import Flask, request
from flask_socketio import SocketIO

from loggingHandler import setup_logging
from groundController import GroundController


setup_logging()

app = Flask(__name__)

# Need to store last command sent
# Button to resume/resend last command (in case of controller invention)
# Controller can shift around blockage
# Website can resend last command to resume

# Instantiate groundController
groundController = GroundController(SocketIO(app))


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return "CS-Ground Flask Server"


@app.route('/testing', methods=['GET'])
def testing():
    return {"body": "Hello World!"}


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


@app.route('/verify-route', methods=['POST'])
def verify_route():
    # Verify route received with route command sent
    json_response = request.get_json()
    return groundController.verify_route(json_response)


@app.route('/verify-command', methods=['POST'])
def verify_command():
    # Verify command received with command sent
    json_response = request.get_json()
    return groundController.verify_command(json_response)


@app.route('/manual-command', methods=['POST'])
def manual_command():
    # Receives form data containing longitude, latitude, priority values
    # Will log command for now
    return


if __name__ == '__main__':
    app.run()
