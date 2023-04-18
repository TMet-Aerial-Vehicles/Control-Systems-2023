import time
from pymavlink import mavutil

# Consistently print received telemetry

# Set up the connection to the autopilot
master = mavutil.mavlink_connection('udp:10.147.20.120:14550')

# Wait for the heartbeat message to find the system ID
master.wait_heartbeat()

# Get the system and component ID to form the target address
system_id = master.target_system
component_id = master.target_component

# Request data for the current state of the vehicle
master.mav.request_data_stream_send(
    master.target_system, master.target_component,
    33, # position
    1, 1)
master.mav.request_data_stream_send(
    master.target_system, master.target_component,
    30, # attitude
    1, 1)
master.mav.request_data_stream_send(
    master.target_system, master.target_component,
    1, # Sys
    1, 1)
# master.mav.command_long_send(
#     master.target_system, master.target_component,
#     mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
#     33, # The MAVLink message ID
#     1e6, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
#     0, 0, 0, 0, # Unused parameters
#     0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
# )

while True:

    # Wait for the next message from the autopilot
    msg1 = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    msg2 = master.recv_match(type='ATTITUDE', blocking=True)
    # msg1, msg2 = None, None
    msg3 = master.recv_match(type='SYS_STATUS', blocking=True)

    # Parse the message and print the relevant data
    if msg1 and msg1.get_type() == 'GLOBAL_POSITION_INT':
        print('Longitude: {}'.format(msg1.lon / 1e7))
        print('Latitude: {}'.format(msg1.lat / 1e7))
        print('Altitude: {} m'.format(msg1.alt / 1000.0))
        print(msg1)
    if msg2 and msg2.get_type() == 'ATTITUDE':
        print('Roll: {} degrees'.format(msg2.roll))
        print('Pitch: {} degrees'.format(msg2.pitch))
        print('Yaw: {} degrees'.format(msg2.yaw))
    if msg3 and msg3.get_type() == 'SYS_STATUS':
        print('Battery Percentage: {}%'.format(msg3.battery_remaining))
    time.sleep(0.25)
    print()
