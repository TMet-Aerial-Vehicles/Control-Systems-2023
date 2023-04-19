from pymavlink import mavutil
import time

# Test taking off and landing

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('udp:127.0.0.1:14552')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))


mode = 'GUIDED'
# Get mode ID
mode_id = the_connection.mode_mapping()[mode]
the_connection.mav.set_mode_send(
    the_connection.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id)
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)
time.sleep(5)


the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)
time.sleep(5)


the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 10)
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

time.sleep(20)

print("Setting mode")
# mode = mavutil.mavlink.MAV_MODE_GUIDED_ARMED
# the_connection.set_mode(mode)
# the_connection.command_long_send(
#     the_connection.target_system, the_connection.target_component,
#     mavutil.mavlink.MAV_CMD_NAV_LAND, # command id
#     0, # confirmation
#     0, 0, 0, 0, 0, 0, 0 # parameters (not used for LAND command)
# )

# Send the SET_MODE command to switch to LAND mode
# mode_id = mavutil.mode_mapping["LAND"]
# the_connection.mav.set_mode_send(
#     the_connection.target_system,
#     mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
#     mode_id
# )
mode = 9 # land

# Create a MSG_SET_MODE message
mode = 'LAND'
print(the_connection.mode_mapping())
# Check if mode is available
if mode not in the_connection.mode_mapping():
    print('Unknown mode : {}'.format(mode))
    print('Try:', list(the_connection.mode_mapping().keys()))

# Get mode ID
mode_id = the_connection.mode_mapping()[mode]
# Set new mode
# master.mav.command_long_send(
#    master.target_system, master.target_component,
#    mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
#    0, mode_id, 0, 0, 0, 0, 0) or:
# master.set_mode(mode_id) or:
the_connection.mav.set_mode_send(
    the_connection.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
time.sleep(5)
