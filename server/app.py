from flask import Flask, jsonify, request
from collections import deque


from qr import AllQr

app = Flask(__name__)
app.config['CORS-HEADERS']: 'Content-Type'


# Fixed size Queue to store telemetry
telemetry = deque([],  maxlen=10)
telemetry.append({
    "longitude": 0,
    "latitude": 0,
    "height": 0,
    "timestamp": 0
})

# Need to store last command sent
# Button to resume/resend last command (in case of controller invention)
# Controller can shift around blockage
# Website can resend last command to resume

# Instantiate and setup QR System
QR_LST = AllQr()


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
    print(json_r)
    raw_qr_str = json_r["raw_qr_string"] if "raw_qr_string" in json_r else None
    qr_type = int(json_r["qr_type"]) if "qr_type" in json_r else None
    if raw_qr_str and qr_type:
        return QR_LST.qrs[qr_type - 1].process(raw_qr_str)

    return {"success": False, "message": "Missing Payload Values"}


@app.route('/get_parsed_qr/<qr_type>', methods=['GET'])
def get_parsed_qr(qr_type):
    # Accepts qr_type
    # Checks if that qr is set in variable
    # Returns success and qr data if found
    if 1 <= int(qr_type) <= 3:
        print("SUCCESSFUL GET")
        return {
            "success": True,
            "qr_type": qr_type,
            "qr_data": QR_LST.qrs[int(qr_type) - 1].convert_to_dict()
        }
    else:
        print("NOT SET")
        return {
            "success": False,
            "message": "Invalid QR Type"
        }


@app.route('/recent-telemetry', methods=['GET'])
def get_recent_telemetry():
    response = jsonify(data=telemetry[-1],
                       success="200")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/set-telemetry', methods=['POST'])
def set_telemetry():

    # Access POST telemetry
    json_r = request.get_json()
    longitude = int(json_r["longitude"]) if "longitude" in json_r else None
    latitude = int(json_r["latitude"]) if "latitude" in json_r else None
    height = int(json_r["height"]) if "height" in json_r else None
    timestamp = int(json_r["timestamp"]) if "timestamp" in json_r else None

    # Verify and Update Telemetry
    if longitude and latitude and height and timestamp:
        telemetry.append({
            "longitude": longitude,
            "latitude": latitude,
            "height": height,
            "timestamp": timestamp
        })
        return {"success": True, "message": "Telemetry Updated"}
    return {"success": False, "message": "Missing Payload Values"}


@app.route('/manual-command', methods=['POST'])
def manual_command():
    # Receives form data containing longitude, latitude, priority values
    # Will log command for now
    return


if __name__ == '__main__':
    app.run()
