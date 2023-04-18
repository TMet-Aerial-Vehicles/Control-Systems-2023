from datetime import datetime
import time
import requests
import logging
from pymavlink import mavutil


class PixhawkController:

    def __init__(self):
        self.vehicle = None
        self.telemetry_thread = None
        self.close_thread = False
        self.current_command = None
        self.command_complete = False
        self.flight_api_connected = False
        self.battery_change_completed = False
        self.telemetry_types = {
            "GLOBAL_POSITION_INT": 33,
            "ATTITUDE": 30,
            "SYS_STATUS": 1
        }
        self.system_id = 0
        self.component_id = 0
        self.starting_latitude = 0
        self.starting_longitude = 0
        self.starting_altitude = 0

    def connect(self, device):
        self.vehicle = mavutil.mavlink_connection(device, baud=115200)
        self.vehicle.wait_heartbeat()
        print("Heartbeat received from Pixhawk")
        logging.info("Connected to Pixhawk")

        self.system_id = self.vehicle.target_system
        self.component_id = self.vehicle.target_component

        # Request telemetry at faster rate
        for value in self.telemetry_types.values():
            self.vehicle.mav.request_data_stream_send(
                self.system_id,
                self.component_id,
                value,
                1,  # Hz
                1
            )

        # Save starting position
        time.sleep(1)   # Wait to allow telemetry stream
        position = self.vehicle.recv_match(type='GLOBAL_POSITION_INT',
                                           blocking=True)
        self.starting_latitude = position.lat / 1e7
        self.starting_longitude = position.lon / 1e7
        self.starting_altitude = position.alt / 1e3

        # # Start telemetry thread
        # self.telemetry_thread = threading.Thread(target=self._get_telemetry)
        # self.telemetry_thread.daemon = True
        # self.telemetry_thread.start()

    def disconnect(self):
        self.close_thread = True
        self.vehicle.close()

    def get_command_ack(self):
        time.sleep(1)
        cmd_resp = self.vehicle.recv_match(type='COMMAND_ACK', blocking=True)
        logging.info(f"\t{cmd_resp}")
        return cmd_resp

    def arm(self):
        print("Arming motors")
        self.vehicle.mav.command_long_send(
            self.system_id,
            self.component_id,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 1, 0, 0, 0, 0, 0, 0)
        return self.get_command_ack()

    def disarm(self):
        print("Disarming motors")
        self.vehicle.mav.command_long_send(
            self.system_id,
            self.component_id,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 0, 0, 0, 0, 0, 0, 0)
        return self.get_command_ack()

    def takeoff(self, altitude):
        print("Taking off to {} meters".format(altitude))
        self.vehicle.mav.command_long_send(
            self.system_id,
            self.component_id,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0, 0, 0, 0, 0, 0, 0, altitude)
        return self.get_command_ack()

    def land(self):
        print("Landing")
        self.vehicle.mav.command_long_send(
            self.vehicle.target_system,
            self.vehicle.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0, 0)
        time.sleep(1)
        return self.get_command_ack()

    def set_mode(self, mode):
        if mode not in self.vehicle.mode_mapping():
            print(f"Unknown mode: {mode}")
            logging.info(f"Unknown mode: {mode}")
            logging.info(f"\tModes: {list(self.vehicle.mode_mapping().keys())}")

        print("Setting mode to {}".format(mode))
        mode_id = self.vehicle.mode_mapping()[mode]
        self.vehicle.mav.set_mode_send(
            self.system_id,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id)
        return self.get_command_ack()

    def go_to_location(self, latitude, longitude, altitude):
        print(f"Going to location: ",
              f"lat={latitude}, lon={longitude}, alt={altitude}")
        self.vehicle.mav.send(
            mavutil.mavlink.MAVLink_set_position_target_global_int_message(
                10, self.vehicle.target_system, self.vehicle.target_component,
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                int(0b110111111000),
                int(latitude * 10**7),
                int(longitude * 10**7),
                altitude,
                0, 0, 0, 0, 0, 0, 0, 0))

    def set_altitude(self, altitude):
        print("Changing altitude to {} meters".format(altitude))
        self.vehicle.mav.command_long_send(
            self.vehicle.target_system,
            self.vehicle.target_component,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 0,
            0, altitude)
        time.sleep(1)

    def get_telemetry(self, blocking=False):
        msg1 = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=blocking)
        msg2 = self.vehicle.recv_match(type='ATTITUDE', blocking=blocking)
        msg3 = self.vehicle.recv_match(type='SYS_STATUS', blocking=blocking)

        # Parse the message and print the relevant data
        telemetry_msg = {
            'latitude': -1,
            'longitude': -1,
            'altitude': -1,
            'roll': -1,
            'yaw': -1,
            'pitch': -1,
            'battery_percentage': -1
        }
        if msg1 and msg1.get_type() == 'GLOBAL_POSITION_INT':
            telemetry_msg["latitude"] = msg1.lat / 1e7
            telemetry_msg["longitude"] = msg1.lon / 1e7
            telemetry_msg["altitude"] = msg1.alt / 1e3
        if msg2 and msg2.get_type() == 'ATTITUDE':
            telemetry_msg["roll"] = msg2.roll
            telemetry_msg["yaw"] = msg2.yaw
            telemetry_msg["pitch"] = msg2.pitch
        if msg3 and msg3.get_type() == 'SYS_STATUS':
            telemetry_msg["battery_percentage"] = msg3.battery_remaining
        telemetry_msg["time"] = datetime.now().strftime("%H:%M:%S %f")
        return telemetry_msg


    def _get_telemetry(self):
        count = 0
        while not self.close_thread:
            count += 0.25
            time.sleep(0.25)
            msg = self.get_telemetry(blocking=True)
            logging.info(msg)

    def return_to_launch(self):
        self.set_mode('RTL')
