from boundingbox import BoundingBox
from shapely import LineString, Point
from waypoint import WAYPOINT_LST
import math
import numpy

#instead of trying to actually make the bounding box, the drone will calculate the shortest route to the rejoin point using the bounding box points as way points.

#waypoints will be a list of Waypoints from the waypoint class
#I need something to keep track of all waypoint distances.
#For the sake of simplicity, The drone will always path to the closest waypoint to the rejoin point. This way it should not cross the boundary of the bounding box.


#basic inverse mercrator from chatgpt
def longlat(x,y):
    lon = x / 20037508.34 * 180.0
    lat = 180.0 / math.pi * (2.0 * math.atan(math.exp(y / 20037508.34 * math.pi)) - math.pi / 2.0)
    return lon,lat

#route will hold bounxing box and rejoin point. it will keep track of the current point in the route as it charts
class route:
    
    #this function will convert the x and y coordinates back to long and lat
    def backtoLongLat(self):
        self.finalRoute = []
        for p in self.evasionRoute:
            x,y = longlat(p.x,p.y)
            wp = Point(x,y)
            self.finalRoute.append(wp)
    
    #trys to reach the rejoin point from the current position. if it can't return false.    
    def try_finish(self):
        line = (Point(self.currentPosition),Point(self.boundingbox.rejoin))
        return not self.boundingbox.checkIntersect(line)
        
    #function responsible for making the evasion route
    #runs recursively until it reaches the rejoin point or reaches the maximum recursion depth and crashes    
    def start_route(self):
        print("Starting evasion route.")
        if(self.try_finish()):
            print("done\n")
            self.evasionRoute.append(Point(self.currentPosition))
            self.evasionRoute.append(Point(self.boundingbox.rejoin))
            #uncomment line below to see the evasion route as it's made
            #self.boundingbox.visualize(self.evasionRoute)
            self.backtoLongLat()
           
            
        else:
            self.evasionRoute.append(Point(self.currentPosition))
            self.currentPosition = self.boundingbox.applyOffset(self.boundingbox.gimme_closest(self.currentPosition))
            self.start_route()
    #function to create lines from the evasion route. This is more for visualization purposes.            
    def create_lines(self):
        self.lines = []
        start = self.evasionRoute[0]
        for p in self.evasionRoute[1:]:
            self.lines.append(LineString(start,p))
            start = p
    #init function. takes in a bounding box and a starting point.
    def __init__(self,boundingbox,start):
        self.evasionRoute = []
        self.currentPosition = []
        start = WAYPOINT_LST.get_wp_by_name(start)
        #delcaring boundingbox to path around
        self.boundingbox = boundingbox
        #converting long and lat to x and y using webmecrator
        self.currentPosition.append(boundingbox.convertX(start.longitude))
        self.currentPosition.append(boundingbox.convertY(start.latitude))
        #begin forming evasion route
        self.start_route()
        
 

