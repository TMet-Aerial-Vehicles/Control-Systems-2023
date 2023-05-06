import configparser
import logging
import requests
import time
import os
import math

from Shared.loggingHandler import setup_logging
from Flight.script.pixhawkController import PixhawkController
from Flight.script.lightController import LightController
from Flight.script.soundController import SoundController


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))
setup_logging(config['Flight_Script']['App_Name'])

FLIGHT_API = f"http://{config['Flight_API']['API_IP_Address']}" + \
             f":{config['Flight_API']['API_IP_PORT']}"


class CommandHandler:

    def __init__(self, pixhawk_controller: PixhawkController,
                 light_controller: LightController,
                 sound_controller: SoundController):
        self.pixhawk = pixhawk_controller
        self.light = light_controller
        self.sound = sound_controller
        self.current_command = {}

    def execute_command(self, command):
        # Commands Accepted:
        #   Takeoff, Navigate, Altitude, Land, RTL, BatteryChange, NavMode,
        #   Brake, Hold, Emergency Land
        if "Command" in self.current_command and \
                self.current_command["Command"] == "Emergency Land":
            time.sleep(30)

        print("Executing Command", command)
        self.current_command = command
        if command["Command"] == "Takeoff":
            print("Setting Guided")
            self.pixhawk.set_mode("GUIDED")
            time.sleep(1)
            print("Arming")
            self.pixhawk.arm()
            print("Takeoff")
            self.pixhawk.takeoff(command["Details"]["Altitude"])
        elif command["Command"] == "Navigate":
            self.pixhawk.go_to_location(command["Details"]["Latitude"],
                                        command["Details"]["Longitude"],
                                        command["Details"]["Altitude"])
        elif command["Command"] == "NavMode":
            self.pixhawk.set_mode("GUIDED")
            time.sleep(1)
        elif command["Command"] == "Brake":
            self.pixhawk.set_mode("BRAKE")
            time.sleep(1)
        elif self.current_command["Command"] == "Altitude":
            self.pixhawk.set_altitude(
                self.current_command["Details"]["Altitude"])
        elif self.current_command["Command"] == "BatteryChange":
            self.sound.play_quick_sound(5)
        elif self.current_command["Command"] == "Hold":
            self.sound.countdown(command["Details"]["Time"])
        elif command["Command"] == "Land":
            # TODO: Use CV for Landing
            self.pixhawk.set_mode("LAND")
        elif command["Command"] == "Qland":
            self.pixhawk.set_mode("QLAND")
        elif command["Command"] == "Emergency Land":
            self.pixhawk.set_mode("LAND")
        elif command["Command"] == "RTL":
            self.pixhawk.set_mode("RTL")

    def is_current_command_completed(self):
        telemetry = self.pixhawk.get_telemetry(blocking=True)

        if self.current_command["Command"] == "Takeoff":
            target_alt = self.current_command["Details"]["Altitude"]
            if target_alt - 0.5 < telemetry['altitude'] < target_alt + 0.5:
                return True
        elif self.current_command["Command"] == "Navigate":
            # TODO: Refactor
            d_lat = self.current_command["Details"]["Latitude"] - telemetry["latitude"]
            d_lon = self.current_command["Details"]["Longitude"] - telemetry["longitude"]
            dist = math.sqrt((d_lat * d_lat) + (d_lon * d_lon)) * 1.113195e5
            if dist < 1:
                return True
        elif self.current_command["Command"] in ["NavMode", "Brake", "Hold"]:
            time.sleep(2)
            return True
        elif self.current_command["Command"] == "Land":
            # TODO: Use CV for Landing
            if -0.5 < telemetry['altitude'] < 0.5:
                return True
        elif self.current_command["Command"] == "RTL":
            if -0.5 < telemetry['altitude'] < 0.5:
                return True
        elif self.current_command["Command"] == "Altitude":
            target_alt = self.current_command["Details"]["Altitude"]
            if target_alt - 0.5 < telemetry['altitude'] < target_alt + 0.5:
                return True
        elif self.current_command["Command"] == "BatteryChange":
            # Wait till button pressed that battery change completed
            try:
                battery_endpoint = "check-for-battery-change-completed"
                response = requests.get(f"{FLIGHT_API}/{battery_endpoint}")
                response.raise_for_status()
                if response.json() and "battery_change_completed" in response.json():
                    bc_status = response.json()["battery_change_completed"]
                    logging.info(f"Battery Change Status: {bc_status}")
                    return bc_status
            except requests.exceptions.RequestException as e:
                logging.error(f"Battery Change Status Error {e}")
                return False

        return False
