import os
import configparser
import logging
import time

from Shared.loggingHandler import setup_logging
from Flight.script.pixhawkController import PixhawkController

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../..', 'config.ini'))
setup_logging(config['Flight_Script']['App_Name'])
print("logging")

FLIGHT_API = f"http://{config['Flight_API']['API_IP_Address']}" + \
             f":{config['Flight_API']['API_IP_PORT']}"
PIXHAWK_CONNECTION_DEVICE = config['Flight_Script']['Pixhawk_Device']
print(PIXHAWK_CONNECTION_DEVICE)

# Initialize all classes needed:
logging.info("Initializing Pixhawk Connection")
pixhawk_controller = PixhawkController()

pixhawk_controller.connect(PIXHAWK_CONNECTION_DEVICE)

pixhawk_controller.connect_to_flight_api(blocking=True)

time.sleep(200)
