from simplified_pixhawkC import PixhawkController
import time

# Assumes starting position is TMU Quad
# Flies to pond, execute 3 times to check fluctuations
# RTL

pixhawk = PixhawkController()
pixhawk.connect("udp:127.0.0.1:14551")

pixhawk.set_mode("GUIDED")
pixhawk.arm()

pixhawk.takeoff(40)

time.sleep(10)

pixhawk.go_to_location(43.6574998,-79.3804078, 80)

time.sleep(10)

pixhawk.go_to_location(43.6574998, -79.3804078, 80)

time.sleep(10)

pixhawk.go_to_location(43.6574998, -79.3804078, 80)

time.sleep(10)

pixhawk.set_mode("RTL")
