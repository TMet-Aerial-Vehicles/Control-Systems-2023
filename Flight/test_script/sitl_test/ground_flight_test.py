import os
import configparser
import logging
import requests
import time

from Shared.loggingHandler import setup_logging
from Flight.server.pixhawkController import PixhawkController

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../..', 'config.ini'))
setup_logging(config['Flight_Script']['App_Name'])

FLIGHT_API = f"http://{config['Ground']['API_IP_Address']}" + \
             f":{config['Ground']['API_IP_PORT']}"

PIXHAWK_CONNECTION_DEVICE = config['Flight_Script']['Pixhawk_Device']

# Initialize all classes needed:
logging.info("Initializing Pixhawk Connection")
pixhawk_controller = PixhawkController()
pixhawk_controller.connect_to_flight_api()

# Get initial route when ready
logging.info("Requesting Initial Route")
initial_route_received = False
routes = None
while not initial_route_received:
    try:
        response = requests.get(f"{FLIGHT_API}/get-initial-route")
        response.raise_for_status()
        if response.json():
            routes = response.json()['route']
            if routes is not None and len(routes) > 0:
                initial_route_received = True

    except requests.exceptions.RequestException as e:
        logging.info("Initial route not received")
        time.sleep(15)

print(routes)

pixhawk_controller.connect(PIXHAWK_CONNECTION_DEVICE)

pixhawk_controller.set_mode("GUIDED")

# Take off
pixhawk_controller.arm()
time.sleep(1)

for route in routes:
    if route['Command'] == "Takeoff":
        pixhawk_controller.takeoff(10)
    elif route['Command'] == "Navigation":
        pixhawk_controller.go_to_location(route['Latitude'], route['Longitude'], 10)
    elif route['Command'] == "Land":
        pixhawk_controller.set_mode("RTL")
    else:
        print("UNKNOWN COMMAND")
