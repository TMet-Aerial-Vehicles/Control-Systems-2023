from collections import deque
from flask_socketio import SocketIO


class TelemetryController:
    def __init__(self, socketio: SocketIO) -> None:
        """Initialize TelemetryController object

        :param socketio: web socket for event notification (SocketIO)
        """
        self.telemetry_data = deque([], maxlen=5)
        self.telemetry_data.append({
            "longitude": 0,
            "latitude": 0,
            "height": 0,
            "timestamp": 0
        })
        self.socketio = socketio

    def extract_and_notify(self, json_r: dict) -> dict:
        """Pull out incoming telemetry and validate. Then notify using event socket

        :param json_r: incoming json data for processing (dict)
        :return: response object specifying status of telemetry parse
        """

        longitude = int(json_r["longitude"]) if "longitude" in json_r else None
        latitude = int(json_r["latitude"]) if "latitude" in json_r else None
        height = int(json_r["height"]) if "height" in json_r else None
        timestamp = json_r["timestamp"] if "timestamp" in json_r else None

        # Verify and Update Telemetry
        if longitude and latitude and height and timestamp:
            new_telem = {
                "longitude": longitude,
                "latitude": latitude,
                "height": height,
                "timestamp": timestamp
            }
            # Notify subscribers with new data
            self.send("telemetry", new_telem)

            return {"success": True, "message": "Telemetry Updated"}

        return {"success": False, "message": "Missing Payload Values"}

    def log_data(self, new_telem: dict) -> None:
        """Append to data Queue, when full drop the oldest elem and append new to end

        :param new_telem: data to be recorded (dict)
        """
        self.telemetry_data.append(new_telem)

    def send(self, event: str, data: dict) -> None:
        """Send data to all subscribers of an event

        :param event: event name (str)
        :param data: object to be emitted during event (dict)
        """
        self.socketio.emit(event, data)
        self.log_data(data)

    def get_recent_data(self) -> dict:
        """Return the latest collected telemetry

        :return dictionary with the latest data stored in telemetry_data
        """
        # -1 represents the last value added to the queue
        return self.telemetry_data[-1]
