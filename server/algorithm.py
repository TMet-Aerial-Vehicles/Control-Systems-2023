from waypoint import WAYPOINT_LST, Waypoint
from route import Route
from utils import calculate_distance
import sys

# Route number 1: 2 pers; Lima; Quebec; 15 kg; obstacle 2 m to NE; $112
# Route number 2: 6 pers; Delta; Charlie; 5 kg; nil; $50
# Route number 3: 4 pers; Alpha; Zulu; 15 kg; other comment; $150"

r_1 = Route(1, 2, "Lima", "Quebec", 15, "Obstacle", 112)
r_2 = Route(2, 6, "Delta", "Charlie", 5, "nil", 50)
r_3 = Route(3, 4, "Alpha", "Zulu", 15, "Comment", 150)
all_routes = [r_1, r_2, r_3]

# [Waypoint_Alpha, Waypoint_Charlie, Waypoint_Zulu]


def get_next_waypoint(current_waypoint: Waypoint, routes: [Waypoint]) -> [(Waypoint, int)]:
    next_possible_waypoints = []
    for i_route in range(len(routes)):
        if routes[i_route].start_waypoint == current_waypoint:
            next_possible_waypoints.append((routes[i_route].end_waypoint, i_route))
        else:
            next_possible_waypoints.append((routes[i_route].start_waypoint, -1))
    return next_possible_waypoints


def compare_optimal_paths(path_1, path_2):
    # path_1 = (reward_1: float, distance_1: float, ratio_1, waypoints_1: [Waypoint])
    # path_2 = (reward_2: float, distance_2: float, ratio_2, waypoints_2: [Waypoint])
    # equal choose money over distance or sm
    if path_1[2] > path_2[2]:
        # Compare path ratios
        return path_1
    elif path_1[2] == path_2[2]:
        # Equal path ratios, return path with smaller distance travelled
        if path_1[1] < path_2[1]:
            return path_1

    return path_2


def calculate_ratio(reward, distance):
    if distance == 0:
        ratio = 0
    else:
        ratio = reward / distance
    return ratio


def calculate_optimized_path(current_waypoint, routes, final_waypoints):
    if not routes:
        # No other starting points left
        return 0, 0, []
    elif len(routes) == 1:
        # 1 Route left, you are at starting position, complete route
        if routes[0].start_waypoint == current_waypoint:
            # ("Reward for Doing Route[0]", "Distance in Making Route[0]")
            return routes[0].reward, routes[0].distance, [routes[0].end_waypoint]
        else:
            # Not at the starting waypoint as the last route
            inter_dist = calculate_distance(current_waypoint, routes[0].start_waypoint)
            return routes[0].reward, inter_dist + routes[0].distance, [routes[0].start_waypoint, routes[0].end_waypoint]

    else:
        # At Lima (current_waypoint)
        next_possible_wp = get_next_waypoint(current_waypoint, routes)

        # wp is waypoint object
        # route_type can either be index of route("Doing Route") or
        # -1 for ("Going to Start of Route")

        # Note: Need to keep track of waypoint chosen when we return
        # Note: Edge case, 2 routes with same start point, should be fine

        calculated_optimized_next = {}
        # More unique here
        for next_wp, route_index in next_possible_wp:

            if final_waypoints and final_waypoints[-1] == next_wp:
                continue

            if route_index != -1:
                # Doing the route
                route_completed = routes.pop(route_index)
                inter_reward, inter_distance, inter_waypoints = calculate_optimized_path(next_wp, routes, [current_waypoint])
                routes.insert(route_index, route_completed)
            else:
                route_completed = Route(-1, 0, current_waypoint.name, next_wp.name, 99999, "", 0)
                inter_reward, inter_distance, inter_waypoints = calculate_optimized_path(next_wp, routes, [current_waypoint])

            inter_ratio = calculate_ratio(inter_reward, inter_distance)
            inter_current_path = (inter_reward + route_completed.reward,
                                  inter_distance + route_completed.distance,
                                  inter_ratio,
                                  [next_wp] + inter_waypoints)
            if next_wp.name in calculated_optimized_next:
                calculated_optimized_next[next_wp.name] = compare_optimal_paths(calculated_optimized_next[next_wp.name],
                                                                                inter_current_path)
            else:
                calculated_optimized_next[next_wp.name] = inter_current_path
        # Want to maximize reward/distance ratio

        # Find highest ratio
        best_path = (-1, 99999, -1/99999, [])

        for name in calculated_optimized_next:
            reward_distance_values = calculated_optimized_next[name]
            best_path = compare_optimal_paths(best_path, reward_distance_values)

        return best_path[0], best_path[1], best_path[3]
        # Go to Quebec, then calculate_optimized_path("Quebec"), + $112, + 5km'

        # Go to Delta, then calculate_optimized_path("Delta"), + $0, +3km

        # Go to Alpha, then calculate_optimized_path("Alpha"), + $0, +3km
        # (reward, distance, routes_passed)


def task_2(all_routes):
    # Pick an initial point

    # Paths must be from route end to another route start
    final_possible_routes = {}

    possible_starts = ["Lima", "Delta", "Alpha"]

    for p_start in possible_starts:
        # Starting Location
        initial_waypoint = WAYPOINT_LST.get_wp_by_name(p_start)

        final_possible_routes[p_start] = calculate_optimized_path(initial_waypoint, all_routes, [])

        # same thing as above
        # calculate max reward, lowest distance for each initial waypoint returned
    best_path_overall = (-1, 99999, -1/99999, [])
    for name in final_possible_routes:
        best_routes_from_name = final_possible_routes[name]
        best_path_overall = compare_optimal_paths(best_path_overall,
                                                  (best_routes_from_name[0],
                                                   best_routes_from_name[1],
                                                   calculate_ratio(best_routes_from_name[0],
                                                                   best_routes_from_name[1]),
                                                   best_routes_from_name[2]))
    return best_path_overall

if __name__ == "__main__":
    # sys.setrecursionlimit(5000)
    stuff = task_2(all_routes)
    print(stuff)
