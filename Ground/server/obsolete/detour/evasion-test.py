from waypoint import WAYPOINT_LST
from Ground.server.obsolete.detour.boundingbox import BoundingBox
from Ground.server.obsolete.detour.route_diversion import DiversionRoute
# from plotGPD import plot

# waypoints = ["Mike","November","Xray","Delta","Foxtrot"]
waypoints = ["Foxtrot", "Whiskey", "Point 18", "Papa", "Bravo"]
definedWaypoints = []
for wp in waypoints:
    definedWaypoints.append(WAYPOINT_LST.get_wp_by_name(name=wp))

rejoin = WAYPOINT_LST.get_wp_by_name("Victor")

trailBox = BoundingBox(definedWaypoints,rejoin)

r = DiversionRoute(trailBox,"Echo")
# plot(r)
