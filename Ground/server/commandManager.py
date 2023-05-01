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
from detourAlgorithm import get_detour_route

from Shared.loggingHandler import setup_logging

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))
setup_logging(config['Ground']['App_Name'])

FLIGHT_API = f"http://{config['Flight_API']['API_IP_Address']}" + \
             f":{config['Flight_API']['API_IP_PORT']}"
# Boolean to email flight plan or send flight plan to drone to execute
TASK_2_EMAIL_DAY = True

# Weight of drone used to filter Task 2 routes with weight limits
VEHICLE_WEIGHT = 7

FLIGHT_ALTITUDE = 80


class CommandManager:

    def __init__(self,
                 qr_handler: QrHandler,
                 telemetry_handler: TelemetryHandler):
        self.qr_handler = qr_handler
        self.telemetry_handler = telemetry_handler

        # For route tracking
        self.waypoint_routes = []
        self.initial_route_plan = []
        self.updated_route_plan = []

    def execute_qr(self, qr_type: QrTypes) -> None:
        """Process QR data and sending initial/updated route to Flight
        Assumes QR data is validated

        :param qr_type: QrTypes enum for which QR data to process
        :return:
        """
        qr_response = self.qr_handler.get_qr(str(qr_type.value),
                                             waypoints_as_dicts=False)
        if not qr_response['success']:
            return
        qr_data = qr_response['qr_data']

        if qr_type == QrTypes.Task_1_Initial_Qr:
            # Save waypoints to be used by Task_1_Update_Qr
            self.waypoint_routes = qr_data["waypoints"]
            self.handle_initial_route_qr(qr_data)
        elif qr_type == QrTypes.Task_1_Update_Qr:
            self.handle_updated_route_qr(qr_data)
        elif qr_type == QrTypes.Task_2_Qr:

            # Filter inaccessible routes
            routes = [route for route in qr_data["routes"]
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

    def handle_initial_route_qr(self, qr_data: dict):
        """
        Handles Task 1 Initial QR. Creates route plan and sends plan to Flight
        Args:
            qr_data: Dict of waypoints in initial route
        Returns: None
        """
        # Create route plan
        plan = [
            {"Command": "Takeoff", "Details": {"Altitude": 80}}
        ]
        for waypoint in qr_data["waypoints"]:
            plan.append(nav_command(waypoint.name, waypoint.latitude,
                                    waypoint.longitude, FLIGHT_ALTITUDE))

        plan.append({"Command": "Land"})

        json_route = {"Route": plan}
        self.initial_route_plan = plan
        print(json_route)

        try:
            response = requests.post(f"{FLIGHT_API}/set-initial-route",
                                     json=json_route)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.info(f"Parse Route - Initial Route POST Error:\n\t{e}")

    def handle_updated_route_qr(self, qr_data: dict):
        """
        Handles Task 1 Update QR. Finds detour around bounding box to the rejoin
        waypoint, and finishes initial route. Sends updated plan to Flight
        Args:
            qr_data: Dict containing boundary and rejoin waypoints
        Returns: None
        """
        # Get detour route to rejoin waypoint
        route_update = self.calculate_detour(qr_data["boundaries"],
                                             qr_data["rejoin_waypoint"])

        # Get rest of route to complete after rejoin
        remaining_waypoints = []
        rejoin_wp_name = qr_data["rejoin_waypoint"].name
        for wp_i in range(len(self.waypoint_routes)):
            if self.waypoint_routes[wp_i].name == rejoin_wp_name:
                remaining_waypoints = self.waypoint_routes[wp_i:]

        # Create flight update message with updated flight plan
        flight_update_msg = {
            "Priority Command": {
                "Command": "Brake",
                "Details": {}
            },
            "Updated Flight Plan": []
        }
        flight_update_msg["Updated Flight Plan"].append(
            {"Command": "NavMode"})

        # Add intermediate waypoints
        for waypoint in route_update:
            flight_update_msg["Updated Flight Plan"].append(
                nav_command(waypoint.name, waypoint.latitude,
                            waypoint.longitude, FLIGHT_ALTITUDE)
            )
        # Add rejoin and remaining waypoints
        for waypoint in remaining_waypoints:
            flight_update_msg["Updated Flight Plan"].append(
                nav_command(waypoint.name, waypoint.latitude,
                            waypoint.longitude, FLIGHT_ALTITUDE)
            )

        # Add final landing
        flight_update_msg["Updated Flight Plan"].append({"Command": "Land"})

        self.updated_route_plan = flight_update_msg
        print(flight_update_msg)

        try:
            response = requests.post(f"{FLIGHT_API}/set-detour-route",
                                     json=flight_update_msg)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.info(f"Parse Route - Detour Route POST Error:\n\t{e}")

    def verify_routes(self, route_type: RouteTypes, routes) -> bool:
        """Validate routes with saved routes

        :param route_type: (RouteTypes) for which Task and initial or updated
        :param routes: Routes to validate with
        :return: True if same routes, else False
        """
        if route_type == RouteTypes.Task_1_Initial_Route:
            return self.initial_route_plan == routes
        elif route_type == RouteTypes.Task_1_Update_Route:
            return self.updated_route_plan == routes
        elif route_type == RouteTypes.Task_2_Route:
            pass

    def calculate_detour(self, boundaries: list[Waypoint],
                         rejoin_waypoint: Waypoint):
        """Calculate intermediate waypoints to detour from current position
         to rejoin waypoint

        :param boundaries: boundary of enclosed by waypoints to avoid
        :param rejoin_waypoint: waypoint to end at
        :return: list of intermediate waypoints
        """
        logging.info(f"Calculating detour to {rejoin_waypoint.name}")
        current_position = self.telemetry_handler.get_recent_data()
        detour_start = Waypoint(name="CurrentPosition", number=1234,
                                longitude=current_position["longitude"],
                                latitude=current_position["latitude"])
        detour_plan = get_detour_route(detour_start, rejoin_waypoint,
                                       boundaries, True)
        return detour_plan


def nav_command(name, latitude, longitude, altitude):
    return {
        "Command": "Navigate",
        "Details": {
            "Latitude": latitude,
            "Longitude": longitude,
            "Altitude": altitude,
            "Name": name
        }
    }
