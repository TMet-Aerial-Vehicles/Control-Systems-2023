import configparser
import logging
import os
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

COORDINATES = [
    (43.648296, -79.406679, 10),
    (43.653145, -79.406149, 10),
    (43.647718, -79.405128, 15),
    (43.654003, -79.400963, 20),
    (43.645895, -79.398889, 25)
]

# Initialize all classes needed:
logging.info("Initializing Pixhawk Connection")
pixhawk_controller = PixhawkController()


pixhawk_controller.connect(PIXHAWK_CONNECTION_DEVICE)

pixhawk_controller.connect_to_flight_api(blocking=True)

pixhawk_controller.set_mode("GUIDED")

# Take off
pixhawk_controller.arm()
time.sleep(1)
pixhawk_controller.takeoff(10)

for i in range(len(COORDINATES)):
    coord = COORDINATES[i]
    pixhawk_controller.go_to_location(coord[0], coord[1], coord[2])

    while not pixhawk_controller.check_command_complete():
        telemetry = pixhawk_controller.get_telemetry()
        if telemetry:
            print(f"Current Position: {telemetry['latitude']}, {telemetry['longitude']}, {telemetry['altitude']}")
        else:
            print("No Telemetry")
        time.sleep(1)

pixhawk_controller.set_mode("RTL")
while not pixhawk_controller.check_command_complete():
    telemetry = pixhawk_controller.get_telemetry()
    print(f"Current Position: {telemetry['latitude']}, {telemetry['longitude']}, {telemetry['altitude']}")
    time.sleep(1)
pixhawk_controller.land()
pixhawk_controller.disarm()
