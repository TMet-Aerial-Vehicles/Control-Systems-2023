from collections import deque

class TelemetryReceiver:
    def __init__(self) -> None:
        self.incoming_data = deque([], maxlen=5)
        self.incoming_data.append({
            "longitude": 0,
            "latitude": 0,
            "height": 0,
            "timestamp": 0
        })
    
    """Append to Queue, when full drop oldest elem and append new to end"""
    def log_data(self, new_telem : dict) -> None:
        self.incoming_data.append(new_telem)