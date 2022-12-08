from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO

from qr import AllQr
from telemetry import TelemetryController

app = Flask(__name__)
CORS(app)

# Need to store last command sent
# Button to resume/resend last command (in case of controller invention)
# Controller can shift around blockage
# Website can resend last command to resume

# Instantiate and setup QR System
QR_LST = AllQr()

# Instantiate a Telemetry Controller
telem_control = TelemetryController(SocketIO(app))

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
    # Saves QR formatted class to QR_LST
    json_r = request.get_json()  # parsable dictionary
    print(f"Received: {json_r}")

    # Access POST request parameters
    raw_qr_str = json_r["raw_qr_string"] if "raw_qr_string" in json_r else None
    qr_type = int(json_r["qr_type"]) if "qr_type" in json_r else None

    # QR Processing
    if raw_qr_str and qr_type:
        if QR_LST.qrs[qr_type - 1].is_valid(raw_qr_str):
            return QR_LST.qrs[qr_type - 1].process(raw_qr_str)
        return {"success": False, "message": f"Invalid QR {qr_type} Format"}

    return {"success": False, "message": "Missing Payload Values"}


@app.route('/get_parsed_qr/<qr_type>', methods=['GET'])
def get_parsed_qr(qr_type):
    # Accepts qr_type
    # Checks if that qr is set in variable
    # Returns success and qr data if found
    if 1 <= int(qr_type) <= 3:
        return {
            "success": True,
            "qr_type": qr_type,
            "qr_data": QR_LST.qrs[int(qr_type) - 1].convert_to_dict()
        }
    else:
        return {
            "success": False,
            "message": "Invalid QR Type"
        }

@app.route('/get-telemetry', methods=['GET'])
def get_telemetry():
    return telem_control.get_recent_data()

@app.route('/set-telemetry', methods=['POST'])
def set_telemetry():

    # Access POST telemetry
    json_r = request.get_json()
    # Process data, and notify event subscribers
    return telem_control.extract_and_notify(json_r)


@app.route('/manual-command', methods=['POST'])
def manual_command():
    # Receives form data containing longitude, latitude, priority values
    # Will log command for now
    return


if __name__ == '__main__':
    app.run()
