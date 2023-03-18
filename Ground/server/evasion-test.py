from waypoint import WAYPOINT_LST
from boundingbox import BoundingBox
from route_diversion import route
from plotGPD import plot

waypoints = ["Mike","November","Xray","Delta","Foxtrot"]
definedWaypoints = []
for wp in waypoints:
    definedWaypoints.append(WAYPOINT_LST.get_wp_by_name(name=wp))
    
rejoin = WAYPOINT_LST.get_wp_by_name("Alpha")

trailBox = BoundingBox(definedWaypoints,rejoin)

r = route(trailBox,"Echo")
plot(r)