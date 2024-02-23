# For TMAV - Landing pad detection and tracking
# Goal: Library can be called using Landing_Pad_Tracking.track() and returns the coordinates of the landing pad
# Author: Tom Croux
# Date: 2021-04-19
# Version: 1.0

# --------------= Sample Use =------------ #

    #from main import Landing_Pad_Tracking

    #LPD = Landing_Pad_Tracking(0)
    #while True :    
        #print(LPD.track())

    # Return -> accuracy, x, y


# --------------= Accuracy =------------ #
#  -> 1.5 : Perfect score
#  -> 1 : Great score
#  -> 0.75 : Good score
#  -> Other : Bad score
#  -> 0 : nothing found
#  -> -1 : Error/nothing found
# -------------------------------------- #

import cv2
import numpy as np

# -------------= Variables =--------------
# For color detection -> initial settings
# orange landing pad!!!! c = [[0, 60, 150], [40, 255, 255]] # minH, minV, minS  maxH, maxV, maxS
c = [[80, 65, 0], [105, 225, 255]] # minH, minV, minS  maxH, maxV, maxS
o = [1.5, 200] # dp, minRadius

# -------------= Main class =--------------
class Landing_Pad_Tracking :

    def __init__(self, camera_id) -> None:
        self.hMin, self.sMin, self.vMin, self.hMax, self.sMax, self.vMax = c[0][0], c[0][1], c[0][2], c[1][0], c[1][1], c[1][2]
        self.dp, self.minDist = o[0], o[1]
        self.cap = cv2.VideoCapture(camera_id)
        
        if (self.cap.isOpened()): 
            print("Video opened")
        else:
            print("Error opening video stream or file")

    # -------------= Track =--------------
    def track(self) :
        try :
            self.success, self.image = self.cap.read() # Capture feed and resize to 1080p
            self.image = cv2.resize(self.image, (1920, 1080))  # Resize frame to 1080p

            # Check if frame is read correctly
            if self.success :
                self.color_detection() # Find the color of the landing pad (blue)
                self.circles_detection() # Find the circular shape of the landing pad 
                self.post_processing() # Post processing to get the center of the landing pad
                self.position() # Calculate the accuracy of the landing pad detection
                return float(self.accuracy), int(self.average_x), int(self.average_y)
            else :
                return -1, 0, 0
        except :
            return -1, 0, 0
            

    # -------------= Color detection =--------------
    def color_detection(self) :
        #self.image = cv2.blur(self.image, (13, 13))
        # Convert to HSV
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        # Define range of orange color in HSV
        lower = np.array([self.hMin, self.sMin, self.vMin])
        upper = np.array([self.hMax, self.sMax, self.vMax])

        mask = cv2.inRange(self.hsv, lower, upper)
        self.color_mask = cv2.bitwise_and(self.image, self.image, mask=mask)

    # -------------= Circles detection =--------------
    def circles_detection(self) :
        # Detect circles
        gray = cv2.cvtColor(cv2.cvtColor(self.color_mask, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY)
        self.circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.5, minDist=1, param1=20, param2=35, minRadius=0, maxRadius=100)

    # -------------= Post processing =--------------
    def post_processing(self) :
        # Get the circles
        if self.circles is not None:
            try :
                # Get the center of the landing pad by averaging the circles
                self.circles = np.round(self.circles[0, :]).astype("int")
                sum_x = 0
                sum_y = 0
                for (x, y, r) in self.circles:
                    sum_x += x
                    sum_y += y
                    #cv2.circle(self.image, (x, y), r, (0, 255, 0), 2)
                    #cv2.putText(self.image, f"{r}", (x, y-r), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

                self.average_x = sum_x / len(self.circles)
                self.average_y = sum_y / len(self.circles)

                # Prepare for kmeans
                criteria = (cv2.TERM_CRITERIA_EPS, 10, 1.0)
                # Set the number of clusters we want to find
                nClusters = 3
                Z = self.circles.astype(np.float32)
                # Apply kmeans
                compactness, label, self.cluster_center = cv2.kmeans(Z,nClusters, None, criteria, 10, cv2.KMEANS_PP_CENTERS )
                for x,y,r in self.cluster_center:
                    #print(f'Cluster center: [{int(x)},{int(y)}]')
                    cv2.rectangle(self.image, (int(x) - int(5), int(y) - 5), (int(x) + 5, int(y) + 5), (0, 0, 255), -1)                
                    cv2.rectangle(self.image, (int(self.average_x) - int(5), int(self.average_y) - 5), (int(self.average_x) + 5, int(self.average_y) + 5), (0, 255, 0), -1)
              
            except :
                return

        else :
            return
    
    # --------------= Accuracy =------------ #
    # Calculate the accuracy of the landing pad detection and return the data
    def position(self) :
        # Calculate the distance between the center of the landing pad and the center of the frame
        x = abs(self.average_x - 1920/2)
        y = abs(self.average_y - 1080/2)
        # Draw a line from the center of the frame to the center of the landing pad
        cv2.line(self.image, (int(1920/2), int(1080/2)), (int(self.average_x), int(self.average_y)), (0, 255, 0), 2)

        # Calculate the accuracy
        self.accuracy = 0
        temp_x,temp_y = 0, 0
        for x,y,r in self.cluster_center:
            offset_x = abs(self.average_x - x)
            offset_y = abs(self.average_y - y)

            # If the offset is less than 30 pixels, add 0.5 to the accuracy
            if offset_x < 30 and offset_y < 30 :
                self.accuracy += 0.5

            # If the offset is less than 100 pixels, add 0.25 to the accuracy
            elif offset_x < 100 and offset_y < 100 :
                self.accuracy += 0.25
            
            # Store the offset of the first circle that is not close enough to the center
            elif temp_x == 0 and temp_y == 0 :
                temp_x = offset_x 
                temp_y = offset_y  

            # If the offset is not the first circle that is not close enough to the center, check if their distance from the center is about the same
            elif (abs(temp_x - offset_x) < 50) and (abs(temp_y - offset_y) < 50) :
                    self.accuracy += 0.25

            # Show text beside each center of cluster_center with their offset from the center of the landing pad
            #cv2.putText(self.image, f"{int(offset_x)}", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Put text distance between the center of the landing pad and the center of the frame
            # So average_x and average_y is the center of the landing pad
            # so something like 1920/2 - average_x is the distance between the center of the frame and the center of the landing pad
            # and do the same for the y axis
            cv2.putText(self.image, f"x = {int(1920/2 - self.average_x)}", (int(1920/2), int(1080/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(self.image, f"y = {int(1080/2 - self.average_y)}", (int(1920/2), int(1080/2) + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Draw a dot in the center of the frame
            cv2.rectangle(self.image, (int(1920/2) - int(5), int(1080/2) - 5), (int(1920/2) + 5, int(1080/2) + 5), (0, 0, 255), -1)

        return
    
# -------------= Development code =--------------
    def dev(self) :
        print("This should only be used for development purposes only!")
        self.name = 'Image'
        cv2.namedWindow(self.name)
        self.trackbar_setup()

        while True:
            self.get_trackbar_pos()
            self.track()

            # Display the resulting frames
            cv2.imshow(self.name, self.image)
            cv2.imshow("Mask", self.color_mask)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    def draw_raw_circles(self) :
        # Get the circles
        if self.circles is not None:
            try :
                self.circles = np.round(self.circles[0, :]).astype("int")
                print("Circle found")
                for (x, y, r) in self.circles:
                    # draw the outer circle
                    cv2.circle(self.color_mask, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(self.color_mask, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            except :
                print("No circles found")
    
    def trackbar_setup(self) :
        # For Color detection
        cv2.createTrackbar('HMin', self.name, 0, 255, self.f)
        cv2.createTrackbar('SMin', self.name, 0, 255, self.f)
        cv2.createTrackbar('VMin', self.name, 0, 255, self.f)
        cv2.createTrackbar('HMax', self.name, 0, 255, self.f)
        cv2.createTrackbar('SMax', self.name, 0, 255, self.f)
        cv2.createTrackbar('VMax', self.name, 0, 255, self.f)

        cv2.setTrackbarPos('HMin', self.name, int(self.hMin))
        cv2.setTrackbarPos('SMin', self.name, int(self.sMin))
        cv2.setTrackbarPos('VMin', self.name, int(self.vMin))
        cv2.setTrackbarPos('HMax', self.name, int(self.hMax))
        cv2.setTrackbarPos('SMax', self.name, int(self.sMax))
        cv2.setTrackbarPos('VMax', self.name, int(self.vMax))

    def f(self, x): pass
    def get_trackbar_pos(self) :
        self.hMin = cv2.getTrackbarPos('HMin', self.name)
        self.sMin = cv2.getTrackbarPos('SMin', self.name)
        self.vMin = cv2.getTrackbarPos('VMin', self.name)

        self.hMax = cv2.getTrackbarPos('HMax', self.name)
        self.sMax = cv2.getTrackbarPos('SMax', self.name)
        self.vMax = cv2.getTrackbarPos('VMax', self.name)

if __name__ == "__main__":
    LPD = Landing_Pad_Tracking("drone.mp4")
    LPD.dev()


