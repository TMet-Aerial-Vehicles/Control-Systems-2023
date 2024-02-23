from main import Landing_Pad_Tracking
import time

LPD = Landing_Pad_Tracking("drone.mp4")
while True :
    print(LPD.track())
    time.sleep(0.01)
