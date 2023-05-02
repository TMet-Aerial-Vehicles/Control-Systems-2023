from pymavlink import mavutil
import time

# Test taking off

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('udp:127.0.0.1:14552')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))

mode_id = the_connection.mode_mapping()['GUIDED']
the_connection.mav.set_mode_send(
    the_connection.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id)
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

# Arm
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)
time.sleep(5)
print("Sending Takeoff")
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 40)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)
