# Controller for Ground component
# Sets up required handlers and managers
# Called by endpoint requests and propagates processing to handlers
import logging
import os
import configparser
from flask_socketio import SocketIO

from qr import QrHandler, QrTypes
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
                self.command_manager.execute_qr(QrTypes(qr_type))
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

    def load_flight_plan_from_file(self):
        """Loads flight plan from file, and sends plan to Flight API
        Returns: API Response
        """
        load_transmit_status = self.command_manager.load_flight_plan_from_file()
        if load_transmit_status:
            return success_dict("Flight Plan Loaded Successfully")
        else:
            return error_dict("Flight Plan Not Loaded. See Logs")

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
