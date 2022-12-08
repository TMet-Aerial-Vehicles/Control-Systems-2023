from collections import deque
from datetime import datetime
from flask_socketio import SocketIO

class TelemetryController:
    def __init__(self, socketio: SocketIO) -> None:
        self.incoming_data = deque([], maxlen=5)
        self.incoming_data.append({
            "longitude": 0,
            "latitude": 0,
            "height": 0,
            "timestamp": 0
        })
        self.socketio = socketio
        self.curr_index = 0

    """Pull out incoming telemetry and validate. Then notify using event socket"""
    def extract_and_notify(self, json_r: dict) -> dict:
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
    
    """Append to Queue, when full drop oldest elem and append new to end"""
    def log_data(self, new_telem : dict) -> None:
        self.incoming_data.append(new_telem)
        self.curr_index = len(self.incoming_data) - 1

    """Send data to all subscribers of an event"""
    def send(self, event: str, data: dict) -> None:
        self.socketio.emit(event, data)
        self.log_data(data)

    """Return the latest collected telemetry"""
    def get_recent_data(self) -> dict:
        return self.incoming_data[self.curr_index]