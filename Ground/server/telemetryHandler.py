from collections import deque
from flask_socketio import SocketIO

from Shared.shared_utils import success_dict, error_dict


class TelemetryHandler:

    def __init__(self, socket_io: SocketIO) -> None:
        """Initialize TelemetryHandler object

        :param socket_io: web socket for event notification (SocketIO)
        """
        self.telemetry_data = deque([], maxlen=5)
        self.telemetry_data.append({
            "longitude": 0,
            "latitude": 0,
            "height": 0,
            "timestamp": 0
        })
        self.socket_io = socket_io

    def extract_and_notify(self, json_r: dict) -> dict:
        """Pull out incoming telemetry and validate.
        Then notify using event socket

        :param json_r: incoming json data for processing (dict)
        :return: response object specifying status of telemetry parse
        """

        longitude = json_r["longitude"] if "longitude" in json_r else None
        latitude = json_r["latitude"] if "latitude" in json_r else None
        height = json_r["altitude"] if "altitude" in json_r else None
        timestamp = json_r["time"] if "time" in json_r else None

        # Verify and Update Telemetry
        if longitude and latitude and timestamp:
            new_telemetry = {
                "longitude": longitude,
                "latitude": latitude,
                "height": height,
                "timestamp": timestamp
            }
            # Notify subscribers with new data
            self.send("telemetry", new_telemetry)
            return success_dict("Telemetry Updated")
        return error_dict("Missing Payload Values")

    def log_data(self, new_telemetry: dict) -> None:
        """Append to data Queue.
        When full, oldest data dropped

        :param new_telemetry: data to be recorded (dict)
        """
        self.telemetry_data.append(new_telemetry)

    def send(self, event: str, data: dict) -> None:
        """Send data to all subscribers of an event

        :param event: event name (str)
        :param data: object to be emitted during event (dict)
        """
        self.socket_io.emit(event, data)
        self.log_data(data)

    def get_recent_data(self) -> dict:
        """Return the latest collected telemetry

        :return dictionary with the latest data stored in telemetry_data
        """
        # -1 represents the last value added to the queue
        return self.telemetry_data[-1]
