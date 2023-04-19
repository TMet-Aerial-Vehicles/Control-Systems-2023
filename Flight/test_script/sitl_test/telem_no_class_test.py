import time
from pymavlink import mavutil

# Set up a connection to the vehicle
vehicle = mavutil.mavlink_connection('udp:127.0.0.1:14549', baud=5200)

# Wait for the heartbeat message to find the system ID
vehicle.wait_heartbeat()
print("heartbeat")

# Request data to be sent at 5 Hz
vehicle.mav.request_data_stream_send(
    vehicle.target_system,
    vehicle.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_ALL,
    1, 1
)

time.sleep(3)

print("Setting guided")
vehicle.set_mode("GUIDED")
time.sleep(3)
# Take off
print("Arming")
vehicle.arducopter_arm()
time.sleep(3)


def takeoff(drone):
    # Arm the drone
    # drone.mav.command_long_send(
    #     drone.target_system, drone.target_component,
    #     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

    # Takeoff to 10 meters
    drone.mav.command_long_send(
        vehicle.target_system,
        vehicle.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 10)

    # Wait for takeoff to complete
    while True:
        msg = drone.recv_match(type=['COMMAND_ACK'])
        if not msg:
            print("No Ack")
            continue
        if msg.command == mavutil.mavlink.MAV_CMD_NAV_TAKEOFF and msg.result:
            print("Ack")
            print(msg)
            break
        time.sleep(0.1)

# def takeoff(vehicle):
#     vehicle.arducopter_arm()
#     time.sleep(1)
#     # vehicle.mav.command_long_send(
#     #     vehicle.target_system,
#     #     vehicle.target_component,
#     #     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 10)
#     takeoff_command = vehicle.message_factory.command_long_encode(
#         0, 0,  # target_system, target_component
#         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,  # command
#         0, 0, 0, 0, 0, 0, 0, 10  # params
#     )
#     vehicle.send_mavlink(takeoff_command)
#     vehicle.flush()
#     time.sleep(1)

taken_off = False
telem_received = False
while True:

    # # Wait for the next message from the vehicle
    # msg = vehicle.recv_match()
    #
    # # If a message has been received, print the telemetry
    # if msg:
    #     print(msg)
    #     if msg.get_type() == 'GLOBAL_POSITION_INT':
    #         print(f'\nLatitude: {msg.lat/1.0e7}, Longitude: {msg.lon/1.0e7}, Altitude: {msg.alt/1.0e3}\n')
    #
    # lat = vehicle.messages['GPS_RAW_INT'].lat / 1e7 if 'GPS_RAW_INT' in vehicle.messages else 0
    # lon = vehicle.messages['GPS_RAW_INT'].lon / 1e7 if 'GPS_RAW_INT' in vehicle.messages else 0
    # alt = vehicle.messages['GLOBAL_POSITION_INT'].alt / 1e3 if 'GLOBAL_POSITION_INT' in vehicle.messages else 0
    # yaw = vehicle.messages['AHRS2'].yaw if 'AHRS2' in vehicle.messages else 0
    # pitch = vehicle.messages['AHRS2'].pitch if 'AHRS2' in vehicle.messages else 0
    # roll = vehicle.messages['AHRS2'].roll if 'AHRS2' in vehicle.messages else 0
    # # mode = vehicle.mode
    # # armable = vehicle.armed
    # system_status = vehicle.messages['SYS_STATUS'].onboard_control_sensors_present if 'SYS_STATUS' in vehicle.messages else 0
    #
    # print(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}, Altitude: {alt:.2f} m")
    # print(f"Yaw: {yaw:.2f}, Pitch: {pitch:.2f}, Roll: {roll:.2f}")
    # # print(f"Mode: {mode}, Armable: {armable}, System status: {system_status}")

    # get position, attitude, and system status messages
    pos_msg = vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    attitude_msg = vehicle.recv_match(type='AHRS2', blocking=True)
    system_status_msg = vehicle.recv_match(type='SYS_STATUS', blocking=True)

    # print out the telemetry data
    if pos_msg and attitude_msg and system_status_msg:
        telem_received = True
        print(f"Latitude: {pos_msg.lat/1e7}, Longitude: {pos_msg.lon/1e7}, Altitude: {pos_msg.alt/1e3}")
        print(f"Roll: {attitude_msg.roll}, Pitch: {attitude_msg.pitch}, Yaw: {attitude_msg.yaw}")
        print(f"Voltage: {system_status_msg.voltage_battery} V, Current: {system_status_msg.current_battery} A")

    msg = vehicle.recv_match(type='SCALED_IMU2', blocking=True)
    if msg is not None:
        print("Motor 1: ", msg.xacc)
        print("Motor 2: ", msg.yacc)
        print("Motor 3: ", msg.zacc)
        print("Motor 4: ", msg.xgyro)
        print("Motor 5: ", msg.ygyro)
        print("Motor 6: ", msg.zgyro)

    time.sleep(1)

    # if not taken_off and telem_received:
    #     time.sleep(5)
    #     print("Commanding Lift off")
    #     takeoff(vehicle)
    #     taken_off = True

