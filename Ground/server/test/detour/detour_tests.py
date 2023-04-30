from Ground.server.waypoint import WaypointList, Waypoint
from Ground.server.detourAlgorithm import get_detour_route

waypoint_lst = WaypointList()
xray = waypoint_lst.get_wp_by_name('Xray')
foxtrot = waypoint_lst.get_wp_by_name('Foxtrot')
point_18 = waypoint_lst.get_wp_by_name('Point 18')
whiskey = waypoint_lst.get_wp_by_name('Whiskey')
papa = waypoint_lst.get_wp_by_name('Papa')
bravo = waypoint_lst.get_wp_by_name('Bravo')
lima = waypoint_lst.get_wp_by_name('Lima')
sierra = waypoint_lst.get_wp_by_name('Sierra')
echo = waypoint_lst.get_wp_by_name('Echo')
kilo = waypoint_lst.get_wp_by_name('Kilo')
charlie = waypoint_lst.get_wp_by_name('Charlie')
romeo = waypoint_lst.get_wp_by_name('Romeo')

# get_detour_route(xray, lima, [foxtrot, point_18, whiskey, papa, bravo], True)
# get_detour_route(romeo, charlie, [echo, foxtrot, xray, kilo], True)

if __name__ == "__main__":
    start = xray
    rejoin = lima
    bounding_box = [foxtrot, point_18, whiskey, papa, bravo]
    detour = get_detour_route(start, rejoin, bounding_box, True)
