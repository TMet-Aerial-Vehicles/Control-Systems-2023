from waypoint import WAYPOINT_LST
from boundingbox import BoundingBox
from route_diversion import DiversionRoute
from plotGPD import plot

waypoints = ["Mike","November","Xray","Delta","Foxtrot"]
definedWaypoints = []
for wp in waypoints:
    definedWaypoints.append(WAYPOINT_LST.get_wp_by_name(name=wp))

rejoin = WAYPOINT_LST.get_wp_by_name("Alpha")

trailBox = BoundingBox(definedWaypoints,rejoin)

r = DiversionRoute(trailBox,"Echo")
plot(r)
