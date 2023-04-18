import os
import configparser
import logging
import requests

from Shared.loggingHandler import setup_logging
from Shared.shared_utils import success_dict, error_dict

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))
setup_logging(config['Flight_API']['App_Name'])

GROUND_API = f"http://{config['Ground']['API_IP_Address']}" + \
             f":{config['Ground']['API_IP_PORT']}"


class FlightController:

    def __init__(self):
        # Need to Track
        # - Entire route plan
        # - Current Command (en route, landing, takeoff
        # - Pixhawk Drone Mode
        # - Priority Command for immediate intent, pauses route plan to do it
        # - Bool for when main route has been recently updated

        # Functionality
        self.route = []
        self.is_route_updated = False   # check if updated since last check
        self.updated_route = []

        self.route_confirmed = False

        self.current_command = {}
        self.commands = []
        self.last_command = ""
        self.priority_command = ""

    def propagate_telemetry(self, json_response: dict):
        resp = requests.post(f"{GROUND_API}/set-telemetry", json=json_response)
        logging.info(resp)
        return success_dict("Sent")

    def set_initial_route(self, json_response: dict):
        # Parse route from json
        route_plan_json = json_response['route']
        if route_plan_json and len(route_plan_json) != 0:
            self.route = route_plan_json
        return {
            "success": True,
            "route": route_plan_json
        }
        # Verify flight plan with ground

        # try:
        #     response = requests.post(f"{GROUND_API}/verify-route",
        #                              json=route_plan)
        #     response.raise_for_status()
        #     if response.json():
        #         self.route_confirmed = True
        #     # Await response, if successful, route confirmed,
        #     # get ready to takeoff
        #     return success_dict("Route Parsed")
        # except requests.exceptions.RequestException as e:
        #     logging.info(f"Parse Route - Verify Route Connection Error:\n\t{e}")
        #     return error_dict(f"Error parsing route: {e}")

    def get_initial_route(self):
        return {
            "success": True,
            "route": self.route
        }

    def set_detour_route(self, json_response: dict):
        # Update next route to
        # Set priority command to brake
        # DO NOT RECOMMENCE NEXT COMMAND TILL ROUTE FULLY UPDATED

        pass
