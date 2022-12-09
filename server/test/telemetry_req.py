import requests
import time
from datetime import datetime

def spam_telemetry():
    url = 'http://127.0.0.1:5000/set-telemetry'
    sample_data = {
        "longitude": "1",
        "latitude": "1",
        "height": "1",
        "timestamp": "1"
    }   

    while True:
        sample_data["timestamp"] = f'{datetime.now()}'
        requests.post(url, json=sample_data)
        time.sleep(0.05) # adjustable time between posts

if __name__ == '__main__':
    spam_telemetry()
