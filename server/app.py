from flask import Flask, jsonify, request

telem = [{
    "longitude": 5,
    "latitude": 6,
    "height": 69,
    "time": 1110
}]
app = Flask(__name__)
app.config['CORS-HEADERS']: 'Content-Type'

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
    jsonResponse = request.get_json()  # parsable dictionary
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
    response = jsonify(data=telem[-1],
                       success="200")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/set-telemetry', methods=['POST'])
def set_telemetry():
    return ("yeet")
    # TODO: make this work


@app.route('/manual-command', methods=['POST'])
def manual_command():
    # Receives form data containing longitude, latitude, priority values
    # Will log command for now
    return


if __name__ == '__main__':
    app.run()
