# Controller for Ground component
# Sets up required handlers and managers
# Called by endpoint requests and propagates processing to handlers
import logging
import os
import configparser
from flask_socketio import SocketIO

from qr import QrHandler, QrTypes
from route import RouteTypes
from telemetryHandler import TelemetryHandler
from boundaryHandler import BoundaryHandler
from commandManager import CommandManager
from Shared.loggingHandler import setup_logging
from Shared.shared_utils import success_dict, error_dict

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))
setup_logging(config['Ground']['App_Name'])


class GroundController:

    def __init__(self, socket_io: SocketIO):
        self.qr_handler = QrHandler()
        self.telemetry_handler = TelemetryHandler(socket_io)
        self.boundary_handler = BoundaryHandler(self.qr_handler,
                                                self.telemetry_handler)
        self.command_manager = CommandManager(self.qr_handler,
                                              self.telemetry_handler)

    def process_qr(self, resp: dict) -> dict:
        """Process QR data from React, saving and processing data into routes

        :param resp: QR data extracted
        :return: API Response
        """
        # Access POST request parameters
        raw_qr_str = resp["raw_qr_string"] if "raw_qr_string" in resp else None
        qr_type = resp["qr_type"] if "qr_type" in resp else None

        # QR Processing
        if raw_qr_str and qr_type:
            qr_response = self.qr_handler.process_qr(qr_type, raw_qr_str)
            logging.info(f"process_qr(): {qr_response['message']}")

            if qr_response["success"]:
                # Send route to flight
                self.command_manager.process_qr(QrTypes(qr_type))
            print("QR Processing Completed")
            return qr_response

        logging.warning("process_qr(): Missing body parameters")
        return error_dict("Missing body parameters")

    def get_qr(self, qr_type: str) -> dict:
        """Get the QR data for qr_type

        :param qr_type: (str) QR to return
        :return: API Response dict containing QR data
        """
        return self.qr_handler.get_qr(qr_type)

    def process_telemetry(self, json_response: dict):
        """Processes telemetry information by updating React and verifying
        drone not nearing boundary

        :param json_response: response containing telemetry
        :return: API Response
        """
        # Save new telemetry data and update subscribers
        self.telemetry_handler.extract_and_notify(json_response)

        # Ensure within boundaries
        # TODO: Handle boundary violation (Not needed for current tasks)
        self.boundary_handler.verify_boundaries()

        return success_dict("Telemetry Received")

    def get_latest_telemetry(self) -> dict:
        """Gets the most recent telemetry stored

        :return: Telemetry data
        """
        return self.telemetry_handler.get_recent_data()

    def verify_route(self, json_response: dict) -> dict:
        """Verifies route received from Flight from Server 1
        If mismatch, resends route to flight

        :param json_response: Route from flight
        :return: API response
        """
        routes = json_response["routes"] if "routes" in json_response else None
        route_type = (json_response["route_type"]
                      if "route_type" in json_response else None)

        if not route_type and routes:
            return error_dict("Missing route parameters")

        try:
            route_type = RouteTypes(int(route_type))
        except ValueError:
            error_msg = "Verify_Route: Unable to identify Route Type Format"
            logging.error(error_msg)
            self.command_manager.send_last_message()
            return error_dict(error_msg)

        if self.command_manager.verify_routes(route_type, routes):
            success_log = "Confirmation routes from Flight verified"
            logging.info(success_log)
            return success_dict(success_log)
        else:
            mismatched_log = f"Mismatched Route from Flight: \n" \
                f"\t Received: {json_response['routes']}\n" \
                f"\t Sent: {self.command_manager.get_sent_command()}\n"
            logging.error(mismatched_log)

            # Send routes to Flight again
            self.command_manager.send_last_message()

    def verify_command(self, json_response: dict):
        pass
