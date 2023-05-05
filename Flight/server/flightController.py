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
        # - Current Command (en route, landing, takeoff)
        # - Pixhawk Drone Mode
        # - Priority Command for immediate intent, pauses route plan to do it
        # - Bool for when main route has been recently updated

        # Functionality
        self.route = []

        self.launch = False

        self.is_route_updated = False   # check if updated since last check
        self.updated_route = []

        self.priority_command = {}
        self.priority_commands_executed = []

        self.battery_change_completed = False

    def propagate_telemetry(self, json_response: dict):
        resp = requests.post(f"{GROUND_API}/set-telemetry", json=json_response)
        logging.info(resp)
        return success_dict("Sent")

    def initiate_launch(self):
        self.launch = True
        return {"initiate_launch": self.launch}

    def check_for_launch(self):
        return {"initiate_launch": self.launch}

    def set_initial_route(self, json_response: dict):
        # Parse route from json
        route_plan_json = json_response["Route"]
        if route_plan_json and len(route_plan_json) != 0:
            self.route = route_plan_json
        return {
            "success": True,
            "route": route_plan_json
        }

    def get_initial_route(self):
        return {
            "success": True,
            "route": self.route
        }

    def get_updated_route(self):
        return {
            "success": True,
            "route": self.updated_route
        }

    def set_detour_route(self, json_response: dict):
        """
        Update the flight plan with new route and priority command
        """
        # Verify json_response
        if "Priority Command" in json_response and \
                "Updated Flight Plan" in json_response:
            # Set priority command
            self.priority_command = json_response["Priority Command"]

            # Set new route
            self.is_route_updated = True
            self.updated_route = json_response["Updated Flight Plan"]
        else:
            return error_dict("Missing JSON Parameters")

    def set_priority_command(self, json_response: dict):
        """
        Send a priority command to execute
        """
        # Verify json_response
        if "Priority Command" in json_response:
            # Set priority command
            self.priority_command = json_response["Priority Command"]
        else:
            return error_dict("Missing JSON Parameters")

    def check_for_route_update(self):
        if self.is_route_updated:
            # Reset after route updated checked
            self.is_route_updated = False

            return {
                "success": True,
                "route_updated": True,
                "route": self.updated_route
            }
        else:
            return {
                "success": True,
                "route_updated": False
            }

    def check_for_priority_command(self):
        """
        Returns priority command if it exists. Resets command after read
        """
        if self.priority_command:
            self.priority_commands_executed.append(self.priority_command)
            return_msg = {
                "success": True,
                "priority_command_created": True,
                "priority_command": self.priority_command
            }
            self.priority_command = {}
            return return_msg
        else:
            return {
                "success": True,
                "priority_command_created": False
            }

    def battery_change_is_complete(self):
        self.battery_change_completed = True
        return {"battery_change_completed": self.battery_change_completed}

    def check_for_battery_change_completed(self):
        return {"battery_change_completed": self.battery_change_completed}
