
import math
import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from waypoint import Waypoint as WP
from waypoint import WAYPOINT_LST
from waypoint import ALL_WAYPOINTS
from shapely.geometry import Polygon, Point, LineString
#NOTE: COORDINATES ARE GIVEN LONG FIRST THEN LAT BY DEFAULT
RADIUS_MAJOR = 6378137.0
RADIUS_MINOR = 6356752.3142
XMAX2D=  20037508.34
YMAX2D=  23810769.32





class BoundingBox:
    def checkIntersect(self,line):
        if not isinstance(line,LineString):
            line = LineString(line)
        if  line.intersects(self.poly):
            return True    
        else:
            return False
    
    def convertX(self,long):
        return math.radians(long)*RADIUS_MAJOR
    
    def convertY(self,lat):
        return math.log(math.tan(math.pi/4 + math.radians(lat)/2))*RADIUS_MAJOR
    
    def to2D(self,rejoin):
        self.rejoin.append(self.convertX(rejoin.longitude))
        self.rejoin.append(self.convertY(rejoin.latitude))
        x = np.zeros(len(self.waypoints))
        y = np.zeros(len(self.waypoints))
        i = 0
        
        for waypoint in self.waypoints:
            x[i] = self.convertX(waypoint.longitude)
            y[i] = self.convertY(waypoint.latitude)
            pt = (x[i],y[i])
            self.points.append(pt)
            i+=1
        self.x = np.array(x)
        self.y = np.array(y)
        self.origin = self.points[0]
        self.drawn_lines = []

    
    
    def visualize(self,route):
        
        x,y = self.poly.exterior.coords.xy
        #fig takes in entire figure while ax takes in individual plots (plt.subplots() returns figure object and array of axes)
        self.fig,self.ax = plt.subplots()
        self.ax.plot(x, y)
        x1 = [p.x for p in route]
        y1 = [p.y for p in route]
        self.ax.plot(x1,y1)
        self.ax.scatter(self.x,self.y)
        self.ax.scatter(x1,y1)
        self.ax.plot(self.rejoin[0],self.rejoin[1],'ro')
        self.ax.set_aspect('equal')
        plt.show()
    
    def gimme_closest(self,point):
        if not isinstance(point, Point):
            point = Point(point)
        closest = Point(self.poly.exterior.coords[0])
        min_dist = point.distance(closest)
        for coord in self.poly.exterior.coords[1:]:
            p = Point(coord)
            dist = point.distance(p)
            if dist < min_dist:
                min_dist = dist
                closest = p
        return closest
        
    def applyOffset(self,p):
        centroid = self.poly.centroid  
        if p.x > centroid.x:
            p = Point(p.x + 10, p.y)
        else:
            p = Point(p.x - 10, p.y)

        if p.y > centroid.y:
            p = Point(p.x, p.y + 10)
        else:
            p = Point(p.x, p.y - 10)
        
        return p
        
    def __init__(self,waypoints,rejoin):
        self.waypoints = waypoints
        self.points = []
        self.rejoin = []
        
        self.to2D(rejoin)
        self.poly = Polygon(self.points)
        self.centroid = self.poly.centroid
    

#trial with QR2:


