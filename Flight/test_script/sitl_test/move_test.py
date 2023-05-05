from pymavlink import mavutil
import time

# Test moving
# Note: Some commands only work on certain SITL

# Start a connection listening to a UDP port
from Shared.shared_utils import get_distance_meters

the_connection = mavutil.mavlink_connection('udp:127.0.0.1:14552')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
print("Heartbeat")
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))

print("Moving")
latitude, longitude, altitude = 48.511464, -71.6491457, 40
lat, lon, alt = 48.511464,-71.6491457, 40
# the_connection.mav.send(
#     mavutil.mavlink.MAVLink_set_position_target_global_int_message(
#         10, the_connection.target_system, the_connection.target_component,
#         mavutil.mavlink.MAV_FRAME_GLOBAL_INT,
#         int(0b110111111000),
#         int(latitude * 10**7),
#         int(longitude * 10**7),
#         altitude,
#         0, 0, 0, 0, 0, 0, 1.57, 0.5))
print("Sent command")
# msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
current_position = the_connection.recv_match(type='GLOBAL_POSITION_INT',
                                           blocking=True)
current_latitude = current_position.lat / 1e7
current_longitude = current_position.lon / 1e7
current_altitude = current_position.alt / 1e3
north_offset, east_offset = get_distance_meters(current_latitude,
                                                current_longitude,
                                                latitude, longitude)
altitude_offset = current_altitude - altitude
# the_connection.mav.send(
#     mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
#         10,
#         the_connection.target_system,
#         the_connection.target_component,
#         mavutil.mavlink.MAV_FRAME_LOCAL_NED,
#         int(0b110111111000),
#         north_offset,
#         east_offset,
#         altitude_offset,
#         0, 0, 0, 0, 0, 0, 0, 0
#     )
# )
#self.vehicle.mav.command_long_send(
#     self.vehicle.target_system,
#    self.vehicle.target_component,
#3    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0,
#    latitude, longitude, altitude)
# the_connection.mav.send(
#     mavutil.mavlink.MAVLink_set_position_target_global_int_message(
#         1000, the_connection.target_system, the_connection.target_component,
#         mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
#         int(0b110111111000),
#         int(-35.3629849 * 10**7),
#         int(149.1649185 * 10**7),
#         20, 0, 0, 0, 0, 0, 0, 1.57, 0.5))
# time.sleep(1)

# msg = mavutil.mavlink.MAVLink_set_position_target_global_int_message(
#     0,                 # time_boot_ms (not used)
#     0,                 # target system (0 for broadcast)
#     0,                 # target component (0 for broadcast)
#     mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
#     0b0000111111000111, # type_mask (only use lat, lon, alt fields)
#     int(lat * 1e7),    # lat (in degrees * 1e7)
#     int(lon * 1e7),    # lon (in degrees * 1e7)
#     alt,               # altitude above sea level (in meters)
#     0,                 # x velocity (not used)
#     0,                 # y velocity (not used)
#     0,                 # z velocity (not used)
#     0,                 # x acceleration (not used)
#     0,                 # y acceleration (not used)
#     0,                 # z acceleration (not used)
#     0,                 # yaw (not used)
#     0)                 # yaw rate (not used)
#
# # Send the message to the drone
# response = the_connection.mav.send(msg)
# print(response)


# Send the message to the drone
# the_connection.send_mavlink(msg)

# while True:
# the_connection.mav.send(
#     mavutil.mavlink.MAVLink_set_position_target_global_int_message(
#         10, the_connection.target_system, the_connection.target_component,
#         mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, int(0b110111111000),
#         int(lat * (10 ** 7)), int(lon * (10 ** 7)), 25, 0, 0, 0, 0, 0, 0, 0, 0))
# # time.sleep(0.25)
# the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,
#                                                                                        the_connection.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, int(0b110111111000), int(-35.3629849 * 10 ** 7), int(149.1649185 * 10 ** 7), 10, 0, 0, 0, 0, 0, 0, 1.57, 0.5))
# #
# the_connection.mav.send(
#     mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
#         10, the_connection.target_system, the_connection.target_component,
#         mavutil.mavlink.MAV_FRAME_LOCAL_OFFSET_NED,
#         int(0b010111111000),
#         0, -200, 5, 0, 0, 0, 0, 0, 0, 0, 0))
mode_id = the_connection.mode_mapping()['GUIDED']
the_connection.mav.set_mode_send(
    the_connection.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id)
time.sleep(3)

print("Sending move")

# the_connection.mav.send(
#     mavutil.mavlink.MAVLink_set_position_target_global_int_message(
#         10, the_connection.target_system, the_connection.target_component,
#         mavutil.mavlink.MAV_FRAME_GLOBAL_INT,
#         int(0b110111111000),
#         int(latitude * 10**7),
#         int(longitude * 10**7),
#         altitude,
#         0, 0, 0, 0, 0, 0, 0, 0))
# Create a SET_POSITION_TARGET_GLOBAL_INT message
print("Actually sending move")
# msg = the_connection.mav.set_position_target_global_int_encode(
#     0, # time_boot_ms (not used)
#     0, 0, # target_system, target_component
#     mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, # frame
#     0b0000111111000111, # type_mask (only positions enabled)
#     int(lat * 1e7), # lat (in degrees * 1e7)
#     int(lon * 1e7), # lon (in degrees * 1e7)
#     int(alt), # alt (in meters)
#     0, 0, 0, # x, y, z velocity (not used)
#     0, 0, 0, # x, y, z acceleration (not used)
#     0, 0) # yaw, yaw_rate (not used)
the_connection.mav.send(
    mavutil.mavlink.MAVLink_set_position_target_global_int_message(
        10,the_connection.target_system, the_connection.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        int(0b110111111000),
        int(latitude * 10**7),
        int(longitude * 10**7),
        altitude,
        0, 0, 0, 0, 0, 0, 0, 0))

# Send the message to the vehicle
# the_connection.mav.send(msg)
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)
# the_connection.mav.set_mode_send(mavutil.mavlink.MAV_MODE_RTL, 0)

# while True:
#     msg = the_connection.recv_match(
#         type='LOCAL_POSITION_NED', blocking=True)
#     print(msg)
#     print(the_connection.messages)
#     for k in the_connection.messages:
#         print(the_connection.messages[k])
the_connection.close()
