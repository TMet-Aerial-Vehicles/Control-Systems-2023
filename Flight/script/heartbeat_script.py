# Checks heartbeat to Ground API
# When connection lost, sends emergency land to Flight API
import configparser
import logging
import requests
import time
import os

from Shared.loggingHandler import setup_logging


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))
setup_logging(config['Flight_Script']['App_Name'])

GROUND_API = f"http://{config['Ground']['API_IP_Address']}" + \
             f":{config['Ground']['API_IP_PORT']}"
FLIGHT_API = f"http://{config['Flight_API']['API_IP_Address']}" + \
             f":{config['Flight_API']['API_IP_PORT']}"

initial_connection_obtained = False
connection_lost_count = 1
while True:
    time.sleep(2)
    try:
        response = requests.get(f"{GROUND_API}/heartbeat")
        response.raise_for_status()
        print("Connection", response.status_code)
        connection_lost_count = 0
    except requests.exceptions.RequestException as e:
        connection_lost_count += 1
        logging.info(f"Heartbeat - Connection Lost:\n\t{e}")
        print(f"ERROR: Connection Lost {connection_lost_count} times")

        if connection_lost_count > 4:
            priority_command = {
                "Priority Command": {"Command": "Emergency Land"}
            }
            try:
                print("ERROR: Connection Lost to Ground for 10 seconds")
                print("ERROR: Sending Emergency Land Priority Command")
                response = requests.post(f"{FLIGHT_API}/set-priority-command",
                                         json=priority_command)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logging.error(f"Heartbeat - Emergency Land Error:\n\t{e}")
