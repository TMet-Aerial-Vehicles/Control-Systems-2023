import configparser
import os
import sys

sys.path.append('../../')

from flask import Flask, request
from Shared.loggingHandler import setup_logging
from flightController import FlightController

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))

app = Flask(__name__)

setup_logging(config['Flight_API']['App_Name'])
flightController = FlightController()


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return "CS-Flight Flask Server"


@app.route('/testing', methods=['GET'])
def testing():
    return {"body": "Hello World! - Flight"}


@app.route('/flight-ready', methods=['GET'])
def flight_ready():
    return {"success": True}


@app.route('/propagate-telemetry', methods=['POST'])
def propagate_telemetry():
    # Called by script, with telemetry data
    # Calls Ground/set-telemetry with same data
    json_response = request.get_json()
    return flightController.propagate_telemetry(json_response)


@app.route('/set-initial-route', methods=['POST'])
def set_initial_route():
    # Called from ground
    # Receives and then calls Ground/verify-route
    json_response = request.get_json()
    return flightController.set_initial_route(json_response)


@app.route('/get-initial-route', methods=['GET'])
def get_initial_route():
    # Called by script
    return flightController.get_initial_route()


@app.route('/launch', methods=['POST'])
def launch():
    # Called by Ground
    return flightController.initiate_launch()


@app.route('/check-for-launch', methods=['GET'])
def check_for_launch():
    # Called by script
    return flightController.check_for_launch()


@app.route('/check-for-route-update', methods=['GET'])
def check_for_update():
    # Called by script
    return flightController.check_for_route_update()


@app.route('/check-for-priority-command', methods=['GET'])
def check_for_priority_command():
    # Called by script
    return flightController.check_for_priority_command()


@app.route('/set-detour-route', methods=['POST'])
def set_detour_route():
    # Called from ground
    # Updates route with detour provided
    json_response = request.get_json()
    return flightController.set_detour_route(json_response)


@app.route('/get-route', methods=['GET'])
def get_route():
    # Called by script
    return {}


@app.route('/update-route', methods=['POST'])
def set_route():
    # Called by ground qr-2
    # Can also be called by website (adaptable)
    return {}


@app.route('/set-command', methods=['POST'])
def set_command():
    # Called by ground
    # Resets saved command (saves to last command)
    return {}


@app.route('/get-command', methods=['GET'])
def get_command():
    # Called by script
    # Resets saved command (saves to last command)
    return {}


if __name__ == '__main__':
    app.run(
        host=config['Flight_API']['API_Local_IP'],
        port=int(config['Flight_API']['API_IP_PORT'])
    )
