import os
import configparser
import logging
import requests
import time

from Shared.loggingHandler import setup_logging
from Flight.server.pixhawkController import PixhawkController

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))
setup_logging(config['Flight_Script']['App_Name'])

FLIGHT_API = f"http://{config['Flight_API']['API_IP_Address']}" + \
             f":{config['Flight_API']['API_IP_PORT']}"
PIXHAWK_CONNECTION_DEVICE = config['Flight_Script']['Pixhawk_Device']

# Initialize all classes needed:
logging.info("Initializing Pixhawk Connection")
pixhawk_controller = PixhawkController()


pixhawk_controller.connect(PIXHAWK_CONNECTION_DEVICE)
