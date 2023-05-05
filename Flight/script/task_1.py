import configparser
import logging
import requests
import time
import os
import sys
sys.path.append('../../')

from Shared.loggingHandler import setup_logging
from Flight.script.pixhawkController import PixhawkController
from Flight.script.commandHandler import CommandHandler
from Flight.script.lightController import LightController
from Flight.script.soundController import SoundController


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))
setup_logging(config['Flight_Script']['App_Name'])

FLIGHT_API = f"http://{config['Flight_API']['API_IP_Address']}" + \
             f":{config['Flight_API']['API_IP_PORT']}"

# Initialize all classes needed:
logging.info("Initializing Pixhawk Connection")
pixhawk = PixhawkController()
lightController = LightController()
soundController = SoundController()
commandHandler = CommandHandler(pixhawk, lightController, soundController)
print("Initialized Controllers")

logging.info("Connecting to Pixhawk")
pixhawk.connect(config['Flight_Script']['Pixhawk_Device'])
logging.info("Connecting to Flight API")
pixhawk.connect_to_flight_api(blocking=True)
print("Connected to Pixhawk and Flight API")


# Get initial route when ready
route = []
logging.info("Requesting Initial Route")
initial_route_received = False
while not initial_route_received:
    try:
        response = requests.get(f"{FLIGHT_API}/get-initial-route")
        response.raise_for_status()
        if response.json() and response.json()["route"] != []:
            route = response.json()["route"]
            logging.info(f"Initial route received:\n\t {route}")
            initial_route_received = True
            # TODO: Validate route

    except requests.exceptions.RequestException as e:
        logging.info(f"Initial route not received {e}")
        time.sleep(5)


# Wait for Initiate signal
initiate_route = False
while not initiate_route:
    try:
        response = requests.get(f"{FLIGHT_API}/check-for-launch")
        response.raise_for_status()
        if response.json() and response.json()["initiate_launch"]:
            initiate_route = True

    except requests.exceptions.RequestException as e:
        logging.info("Waiting for Initiate")
        time.sleep(1)

# Initiating
print("Launching in 10 seconds")
soundController.countdown(9)
soundController.play_quick_sound(4)
logging.info("Launching")
print("Launching")

# Route Execution Loop
route_index = 0
executing_priority_command = False
current_command_sent = False
while True:
    current_command = route[route_index]

    # Send command to Pixhawk
    if not current_command_sent:
        print("Executing ", current_command)
        logging.info(f"Executing: {current_command}")
        commandHandler.execute_command(current_command)
        current_command_sent = True

    # Check if priority command received, execute immediately
    try:
        response = requests.get(f"{FLIGHT_API}/check-for-priority-command")
        response.raise_for_status()
        if response.json() and "priority_command" in response.json():
            priority_cmd_exists = response.json()["priority_command_created"]
            if priority_cmd_exists:
                priority_cmd = response.json()["priority_command"]
                logging.info(f"Executing Priority Command: {priority_cmd}")
                commandHandler.execute_command(priority_cmd)
                executing_priority_command = True
                # Hold after priority command to stabilize/finish
                time.sleep(5)
    except requests.exceptions.RequestException as e:
        logging.info("Unable to check for priority command", e)

    # Check if route updated
    try:
        response = requests.get(f"{FLIGHT_API}/check-for-route-update")
        response.raise_for_status()
        if response.json():
            route_updated = response.json()["route_updated"]
            if route_updated:
                logging.info("Updated Route Received")
                route = response.json()["route"]
                route_index = 0
                commandHandler.execute_command(route[route_index])
    except requests.exceptions.RequestException as e:
        logging.info("Unable to check for update", e)

    # Check if current command completed
    if commandHandler.is_current_command_completed():
        print("Command Completed")
        if not executing_priority_command:
            print("Executing next command")
            route_index += 1
        else:
            executing_priority_command = False
        current_command_sent = False
    else:
        print("\tCommand not completed")
