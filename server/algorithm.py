from waypoint import WAYPOINT_LST, Waypoint
from route import Route
from utils import calculate_distance

def count_waypoint_occurances(curr_wp: Waypoint, final_waypoints: list[Waypoint]) -> int:
    return len([wp for wp in final_waypoints if wp.name == curr_wp.name])


def get_next_waypoint(current_waypoint: Waypoint, routes: list[Waypoint]) -> list[(Waypoint, int, bool)]:
    next_possible_waypoints = []
    for i_route in range(len(routes)):
        if routes[i_route].start_waypoint == current_waypoint:
            next_possible_waypoints.append((routes[i_route].end_waypoint, i_route, True))
        else:
            next_possible_waypoints.append((routes[i_route].start_waypoint, i_route, False))
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
        # Calculate dist to return to origin final_waypoints[0]
        return_dist = calculate_distance(routes[0].end_waypoint, final_waypoints[0])
        if routes[0].start_waypoint == current_waypoint:
            # 1 Route left, you are at starting position, complete route
            return routes[0].reward, routes[0].distance + return_dist, [routes[0].end_waypoint, final_waypoints[0]]
        else:
            # Not at the starting waypoint as the last route
            inter_dist = calculate_distance(current_waypoint, routes[0].start_waypoint)
            return routes[0].reward, inter_dist + routes[0].distance + return_dist, \
                [routes[0].start_waypoint, routes[0].end_waypoint, final_waypoints[0]]
        # ("Reward for Doing Route[0]", "Distance in Completing Route[0] + Return to origin", Waypoints)

    else:
        next_possible_wp = get_next_waypoint(current_waypoint, routes)

        calculated_optimized_next = {}
        
        for next_wp, route_index, at_start_wp in next_possible_wp:
        
            if at_start_wp:
                # Doing the route
                route_completed = routes.pop(route_index)
                inter_reward, inter_distance, inter_waypoints = calculate_optimized_path(next_wp, routes, final_waypoints + [current_waypoint])
                routes.insert(route_index, route_completed)
            else:
                max_wp_threshold = 2
                if count_waypoint_occurances(next_wp, final_waypoints) < max_wp_threshold:
                    # If waypoint has not been passed more than twice, go to waypoint (configurable)
                    route_completed = Route(-1, 0, current_waypoint.name, next_wp.name, 99999, "", 0)
                    inter_reward, inter_distance, inter_waypoints = calculate_optimized_path(next_wp, routes, final_waypoints + [current_waypoint])
                else:
                    # skip next_wp option if it has been passed more than twice
                    continue

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

        # reward, distance, ratio, waypoints
        best_path = (-1, 99999, -1/99999, [])

        for name in calculated_optimized_next:
            reward_distance_values = calculated_optimized_next[name]
            best_path = compare_optimal_paths(best_path, reward_distance_values)

        return best_path[0], best_path[1], best_path[3]


def task_2():
    # Sample Starting Point
    start_wp = WAYPOINT_LST.get_wp_by_name("Origin")

    # Route number 1: 2 pers; Lima; Quebec; 15 kg; obstacle 2 m to NE; $112
    # Route number 2: 6 pers; Delta; Charlie; 5 kg; nil; $50
    # Route number 3: 4 pers; Alpha; Zulu; 15 kg; other comment; $150"
    r_1 = Route(1, 2, "Lima", "Quebec", 15, "Obstacle", 112)
    r_2 = Route(2, 6, "Delta", "Charlie", 5, "nil", 50)
    r_3 = Route(3, 4, "Alpha", "Zulu", 15, "Comment", 150)
    all_routes = [r_1, r_2, r_3]

    reward, dist, waypoints = calculate_optimized_path(start_wp, all_routes, [start_wp])

    return [start_wp] + waypoints

if __name__ == "__main__":
    # sys.setrecursionlimit(5000)
    stuff = task_2()
    print(stuff)
