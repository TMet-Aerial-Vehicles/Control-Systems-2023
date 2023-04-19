import configparser
import logging
import requests
import time
import os

from Shared.loggingHandler import setup_logging
from Flight.script.pixhawkController import PixhawkController
from Flight.script.commandHandler import CommandHandler


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../..', 'config.ini'))
setup_logging(config['Flight_Script']['App_Name'])

FLIGHT_API = f"http://{config['Ground']['API_IP_Address']}" + \
             f":{config['Ground']['API_IP_PORT']}"

# Initialize all classes needed:
logging.info("Initializing Pixhawk Connection")
pixhawk = PixhawkController()
logging.info("Initializing CommandHandler")
commandHandler = CommandHandler(pixhawk)

logging.info("Connecting to Pixhawk")
pixhawk.connect("udp:10.147.20.120:14551")

time.sleep(5)

print("Executing Takeoff")
commandHandler.execute_command({"Command": "Takeoff",
                                "Details": {"Altitude": 40}})
while not commandHandler.is_current_command_completed():
    print("\tTaking off")
print("FINISHED TAKE OFF COMMAND")

time.sleep(3)

print("Executing Navigate to Delta")
commandHandler.execute_command({"Command": "Navigate",
                                "Details": {
                                    "Latitude": 48.5150341,
                                    "Longitude": -71.6404442,
                                    "Altitude": 40}})
while not commandHandler.is_current_command_completed():
    print("\tNavigating")
print("FINISHED NAVIGATION COMMAND")

print("Executing Navigate to Delta")
commandHandler.execute_command({"Command": "Navigate",
                                "Details": {
                                    "Latitude": 48.4921159,
                                    "Longitude": -71.6340069,
                                    "Altitude": 40}})
while not commandHandler.is_current_command_completed():
    print("\tNavigating")
print("FINISHED NAVIGATION COMMAND")

print("Executing Navigate")
commandHandler.execute_command({"Command": "RTL"})
while not commandHandler.is_current_command_completed():
    print("\tReturning")
print("FINISHED RETURNING TO LAUNCH COMMAND")
