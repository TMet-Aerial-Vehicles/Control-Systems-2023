from flask import Flask, jsonify, request

app = Flask(__name__)

plan = None
telemetry = []  # Fixed size queue?


@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return "Hello World!"


@app.route('/testing', methods=['GET'])
def testing():
    return {"body": "Hello World!"}


@app.route('/task-1', methods=['GET'])
def task_1():
    return


@app.route('/task-2', methods=['GET'])
def task_2():
    return


@app.route('/validate-qr', methods=['POST'])
def validate_qr():
    # Accepts 2 form parameters, raw_qr_string and qr_type (enum)
    # Checks format of raw_qr_string if it conforms to the type
    # Saves QR formatted class to variable
    # Returns success if valid
    jsonResponse = request.get_json() # parsable dictionary
    print(jsonResponse)
    return {'status': 'SUCCESS'}


@app.route('/get_parsed_qr/<qr_type>', methods=['GET'])
def get_parsed_qr(qr_type):
    # Accepts qr_type
    # Checks if that qr is set in variable
    # Returns success and qr data if found
    return {
        'status': 'SUCCESS',
        'qr_type': qr_type,
        'qr_data': ""
    }


@app.route('/recent-telemetry', methods=['GET'])
def get_recent_telemetry():
    # Gets latest telemetry info from variable queue
    # queue.pop() to receive latest telemetry and return to react
    return jsonify(
        data={"success": True, 'telemetry': 123},
        status=200
    )


@app.route('/manual-command', methods=['POST'])
def manual_command():
    # Receives form data containing longitude, latitude, priority values
    # Will log command for now
    return


if __name__ == '__main__':
    app.run()
