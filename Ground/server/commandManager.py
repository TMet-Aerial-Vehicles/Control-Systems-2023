# Manager for sending and verifying route commands
import json
import logging
import configparser
import requests
import os
from qr import QrTypes, QrHandler
from telemetryHandler import TelemetryHandler
from route import RouteTypes
from waypoint import Waypoint
from algorithm import task_2, format_for_execute_command

from Shared.loggingHandler import setup_logging

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))
setup_logging(config['Ground']['App_Name'])

FLIGHT_API = f"http://{config['Flight_API']['API_IP_Address']}" + \
             f":{config['Flight_API']['API_IP_PORT']}"
# Boolean to email flight plan or send flight plan to drone to execute
TASK_2_EMAIL_DAY = True

# Weight of drone used to filter Task 2 routes with weight limits
VEHICLE_WEIGHT = 0


class CommandManager:

    def __init__(self,
                 qr_handler: QrHandler,
                 telemetry_handler: TelemetryHandler):
        self.qr_handler = qr_handler
        self.telemetry_handler = telemetry_handler
        self.route = []
        self.updated_route = []
        self.current_command = None
        self.backup_command = None
        self.sent_command = None
        self.sent_message = ""

    def connect_to_socket(self):
        """Start socket connection

        :return: True if successful connection, else False
        """
        # return self.socket.connect()
        return True

    def send_command(self, message):
        """Send message to Flight

        :param message: (str) message to send
        :return: True if successful send, else False
        """
        # status = self.socket.send_message(message)
        status = True
        self.sent_message = message if status else self.sent_message
        return status

    def send_last_message(self):
        """Send last recorded message

        :return: True if successful send, else False
        """
        # return self.socket.send_message(self.sent_message)
        return True

    def send_initial_route(self):
        pass

    def send_updated_route(self):
        pass

    def process_qr(self, qr_type: QrTypes) -> None:
        """Process QR data and sending initial/updated route to Flight
        Assumes QR data is validated

        :param qr_type: QrTypes enum for which QR data to process
        :return:
        """
        qr_response = self.qr_handler.get_qr(str(qr_type.value),
                                             waypoints_as_dicts=True)
        if not qr_response['success']:
            return
        qr_data = qr_response['qr_data']

        if qr_type == QrTypes.Task_1_Initial_Qr:
            # Create route plan
            plan = [
                {"Command": "Takeoff", "Details": {"Altitude": 80}}
            ]
            for waypoint in qr_data["waypoints"]:
                plan.append(
                    {
                        "Command": "Navigation",
                        "Details:": {
                            "Latitude": waypoint["latitude"],
                            "Longitude": waypoint["longitude"],
                            "Altitude": 80,
                            "Name": waypoint["name"]
                        }
                    })
            plan.append({"Command": "RTL"})

            json_route = {"route": plan}
            self.route = plan
            print(json_route)

            try:
                response = requests.post(f"{FLIGHT_API}/set-initial-route",
                                         json=json_route)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logging.info(f"Parse Route - Initial Route POST Error:\n\t{e}")

        elif qr_type == QrTypes.Task_1_Update_Qr:
            # Maybe BoundaryHandler class should calculate detour?
            route_update = self.calculate_detour(qr_data.boundaries,
                                                 qr_data.rejoin_waypoint)
            wp_upd_str = f"{route_update}"
            message = f"QR2:{wp_upd_str}"
            # self.socket.send_message(message)

        elif qr_type == QrTypes.Task_2_Qr:
            flight_plan_route = qr_data.routes

            # Filter inaccessible routes
            routes = [route for route in qr_data.routes
                      if route.max_vehicle_weight > VEHICLE_WEIGHT]

            if TASK_2_EMAIL_DAY:
                # Optimization algorithm
                flightplan = task_2(routes)

                # Save to json
                flight_instructions = format_for_execute_command(flightplan)
                json_obj = json.dumps(flight_instructions, indent=4)
                with open("task2.json", "w") as outfile:
                    outfile.write(json_obj)

                # Send email with route plan
                comp_email = flightplan.generate_email()
                # TODO: Send email https://stackoverflow.com/questions/6270782/how-to-send-an-email-with-python 

            else:
                # Read flight plan from file
                with open('task2.json', "r") as openfile:
                    flight_instructions = json.load(openfile)

                # Send flight plan to Flight
                # TODO: Update with latest communication using str(flight_instructions)
                # self.socket.send_message(f"QR3:{str(flight_instructions)}")

    def verify_routes(self, route_type: RouteTypes, routes) -> bool:
        """Validate routes with saved routes

        :param route_type: (RouteTypes) for which Task and initial or updated
        :param routes: Routes to validate with
        :return: True if same routes, else False
        """
        if route_type == RouteTypes.Task_1_Initial_Route:
            return self.route == routes
        elif route_type == RouteTypes.Task_1_Update_Route:
            pass
        elif route_type == RouteTypes.Task_2_Route:
            pass

    def get_sent_command(self) -> str:
        """Retrieve last sent command message

        :return: (str) command message
        """
        return self.sent_command

    def calculate_detour(self, boundaries: list[Waypoint],
                         rejoin_waypoint: Waypoint):
        """Calculate detour from current position to rejoin waypoint

        :param boundaries: boundary of enclosed by waypoints to avoid
        :param rejoin_waypoint: waypoint to end at
        :return:
        """
        # TODO: Finish detour
        logging.info(f"Calculating detour to {rejoin_waypoint.name}")
        detour_start = self.telemetry_handler.get_recent_data()
        detour_end = rejoin_waypoint
        return boundaries, detour_start, detour_end
