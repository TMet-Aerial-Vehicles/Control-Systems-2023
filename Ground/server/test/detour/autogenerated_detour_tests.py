from Ground.server.waypoint import ALL_WAYPOINTS, Waypoint
from Ground.server.detourAlgorithm import get_detour_route

from random import randint


def get_unselected_waypoint(waypoints_lst, selected_waypoints):
    potential_wp = waypoints_lst[randint(0, len(waypoints_lst) - 1)]
    if potential_wp in selected_waypoints:
        print("Duplicate waypoint...re-selecting")
        return get_unselected_waypoint(waypoints_lst, selected_waypoints)
    return potential_wp

if __name__ == "__main__":
    waypoints_lst = ALL_WAYPOINTS.copy()

    # Get random starting and rejoin waypoint
    start_wp = get_unselected_waypoint(waypoints_lst, [])
    rejoin_wp = get_unselected_waypoint(waypoints_lst, [start_wp])

    # Choose a random number of waypoints to use for bounding box
    num_bbox_points = randint(3, 6)

    # Choose random waypoints to use for bounding box
    bbox_waypoints = []
    for i in range(num_bbox_points):
        wp = get_unselected_waypoint(waypoints_lst,
                                     bbox_waypoints + [start_wp, rejoin_wp])
        bbox_waypoints.append(wp)

    print("Start:", start_wp)
    print("Rejoin:", rejoin_wp)
    print("Bounding Box", bbox_waypoints)
    get_detour_route(start_wp, rejoin_wp, bbox_waypoints, True)
