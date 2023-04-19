import configparser
import logging
import requests
import time
import os

from commandHandler import CommandHandler
from Shared.loggingHandler import setup_logging
from Flight.server.pixhawkController import PixhawkController


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))
setup_logging(config['Flight_Script']['App_Name'])

FLIGHT_API = f"http://{config['Ground']['API_IP_Address']}" + \
             f":{config['Ground']['API_IP_PORT']}"

# Initialize all classes needed:
logging.info("Initializing Pixhawk Connection")
pixhawk = PixhawkController()
logging.info("Initializing CommandHandler")
commandHandler = CommandHandler(pixhawk)
logging.info("Initializing Light Controller")
# - LightController


# Get initial route when ready
route = []
logging.info("Requesting Initial Route")
initial_route_received = False
while not initial_route_received:
    try:
        response = requests.get(f"{FLIGHT_API}/get-initial-route")
        response.raise_for_status()
        if response.json():
            route = response.json()["route"]
            logging.info(f"Initial route received:\n\t {route}")
            initial_route_received = True
            # TODO: Validate route

    except requests.exceptions.RequestException as e:
        logging.info("Initial route not received")
        time.sleep(5)


# Wait for Initiate signal
initiate_route = False
while not initiate_route:
    try:
        response = requests.get(f"{FLIGHT_API}/check-for-initiate")
        response.raise_for_status()
        if response.json() and response.json()["initiate"] == True:
            initiate_route = True

    except requests.exceptions.RequestException as e:
        logging.info("Waiting for Initiate")
        time.sleep(0.5)

# TODO: Add Sound
time.sleep(10)
logging.info("Launching")


# Route Execution Loop
route_index = 0
executing_priority_command = False
current_command_sent = False
while True:
    current_command = route[route_index]

    # Hold/Loiter Commands may need to be processed here to not lose process

    # Send command to Pixhawk
    if not current_command_sent:
        commandHandler.execute_command(current_command)
        current_command_sent = True

    # Check if priority command received, execute immediately
    try:
        response = requests.get(f"{FLIGHT_API}/check-for-priority-command")
        response.raise_for_status()
        if response.json():
            priority_command = response.json()["priority_command"]
            if priority_command:
                logging.info(f"Executing Priority Command")
                commandHandler.execute_command(priority_command)
                executing_priority_command = True
                # Hold after priority command to stabilize
                time.sleep(3)
    except requests.exceptions.RequestException as e:
        logging.info("Unable to check for priority command", e)

    # Check if route updated
    try:
        response = requests.get(f"{FLIGHT_API}/check-for-route-update")
        response.raise_for_status()
        if response.json():
            route_updated = response.json()['Route Updated']
            if route_updated:
                logging.info("Updated Route Received")
                route = response.json()['route']
                route_index = 0
                commandHandler.execute_command(route[route_index])
    except requests.exceptions.RequestException as e:
        logging.info("Unable to check for update", e)

    # Check if current command completed
    if commandHandler.is_current_command_completed():
        if not executing_priority_command:
            route_index += 1
        else:
            executing_priority_command = False
        current_command_sent = False

# Pseudo
# While route not complete or not error:
# Get route
# - Set up end goal
# Get command
# If not takeoff,
# Wait for Takeoff command
# If takeoff
# Countdown(30sec w sound)
# Call pixhawk takeoff
#
# Set to guided mode
# Send gps coordinates to pixhawk
# While not there yet,
# wait and send telemetry
# Get route from API to check changes
# Check if need to cancel current route
# If there,
# If task 1, set up next route
#
#
#
# If task 2
# Land
# Countdown
# Takeoff
# Set up next route
#
#
#
