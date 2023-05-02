from pymavlink import mavutil
import time

# Start a connection listening to a UDP port
print("Connecting")
the_connection = mavutil.mavlink_connection('udp:10.147.20.120:14551')
print("Waiting Heartbeat")
# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))
print("Connected")
# Arm
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

# Wait for Response
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

time.sleep(10)

# Disarm
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

time.sleep(10)
