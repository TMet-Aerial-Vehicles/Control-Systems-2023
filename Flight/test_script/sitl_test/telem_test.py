from pymavlink import mavutil
import time

# Start a connection listening to a UDP port
vehicle = mavutil.mavlink_connection('udpout:127.0.0.1:14445')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
vehicle.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (vehicle.target_system, vehicle.target_component))

request = vehicle.mav.request_data_stream_send(
    vehicle.target_system,
    vehicle.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_ALL,
    1, 1
)
print(request)

start_time = time.time()
while True:
    now = time.time()
    print("-----------> Elapsed Time: ", now - start_time)
    # msg_types = ['GLOBAL_POSITION_INT', 'AHRS2', 'SYS_STATUS']
    # for msg_type in msg_types:
    #     msg = vehicle.recv_match(type=msg_type, blocking=False)
    # # if msg.get_type() == 'GLOBAL_POSITION_INT':
    # #     # Handle GLOBAL_POSITION_INT message
    # #     print("Global Position Int: %s" % msg)
    # # elif msg.get_type() == 'AHRS2':
    # #     # Handle AHRS2 message
    # #     print("AHRS2: %s" % msg)
    #     print(msg)
    # time.sleep(2)
    # print()

    msg = vehicle.recv_match(type=['GLOBAL_POSITION_INT', 'AHRS2', 'SYS_STATUS', 'ATTITUDE'], blocking=True)
    if not msg:
        continue
    # process message
    if msg.get_type() == 'GLOBAL_POSITION_INT':
        print(f"Altitude: {msg.alt / 1000} meters")
    elif msg.get_type() == 'SYS_STATUS':
        print(f"Battery Voltage: {msg.voltage_battery / 1000} V")
    elif msg.get_type() == 'AHRS2':
        print(msg)
    elif msg.get_type() == 'ATTITUDE':
        print(msg)
    # wait for 1 second
    time.sleep(1)
    print()

    # get position, attitude, and system status messages

    # pos_msg = vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    # attitude_msg = vehicle.recv_match(type='AHRS2', blocking=True)
    # system_status_msg = vehicle.recv_match(type='SYS_STATUS', blocking=True)

    # # print out the telemetry data
    # if pos_msg and attitude_msg and system_status_msg:
    #     telem_received = True
    #     print(f"Latitude: {pos_msg.lat/1e7}, Longitude: {pos_msg.lon/1e7}, Altitude: {pos_msg.alt/1e3}")
    #     print(f"Roll: {attitude_msg.roll}, Pitch: {attitude_msg.pitch}, Yaw: {attitude_msg.yaw}")
    #     print(f"Voltage: {system_status_msg.voltage_battery} V, Current: {system_status_msg.current_battery} A")
    #
    # msg = vehicle.recv_match(type='SCALED_IMU2', blocking=True)
    # if msg is not None:
    #     print("Motor 1: ", msg.xacc)
    #     print("Motor 2: ", msg.yacc)
    #     print("Motor 3: ", msg.zacc)
    #     print("Motor 4: ", msg.xgyro)
    #     print("Motor 5: ", msg.ygyro)
    #     print("Motor 6: ", msg.zgyro)
    #
    # time.sleep(1)
