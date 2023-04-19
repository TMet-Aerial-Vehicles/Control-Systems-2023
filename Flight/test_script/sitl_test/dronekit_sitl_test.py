import time
from pymavlink import mavutil

# Connect to the SITL vehicle
connection_string = 'tcp:127.0.0.1:5760'
master = mavutil.mavlink_connection(connection_string)

# Set the system and component ID
system_id = 1
component_id = 1

# Arm the vehicle
master.arducopter_arm()

# Set mode to GUIDED
print("Setting mode")
mode = mavutil.mavlink.MAV_MODE_GUIDED_ARMED
master.set_mode(mode)

print("Takeoff")
# Take off to 10m altitude
target_altitude = 10
master.mav.command_long_send(
    system_id, component_id,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0, 0, 0, 0, 0, 0, 0, target_altitude)

# Wait until the vehicle reaches target altitude
while True:
    msg = master.recv_match(type='STATUSTEXT', blocking=True, timeout=1)
    if msg and 'MODE:' in msg.text:
        mode = msg.text.split('MODE: ')[1].strip()
        print(mode)
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
    alt = msg.alt / 1000.0 if msg else 0
    print('Current altitude: {} m'.format(alt))
    if alt >= target_altitude:
        break
    time.sleep(1)

# Print message when the drone reaches target altitude
print('Target altitude reached: {} m'.format(target_altitude))

# Set mode to LAND
master.set_mode_px4('LAND', system_id, component_id)

# Wait until the vehicle lands
while True:
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    alt = msg.alt / 1000.0
    print('Current altitude: {} m'.format(alt))
    if alt <= 0.2:  # Check for 20 cm altitude for safety
        break
    time.sleep(1)

# Disarm the vehicle
master.arducopter_disarm()
