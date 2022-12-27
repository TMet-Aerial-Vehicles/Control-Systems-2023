from waypoint import WAYPOINT_LST, Waypoint
from route import Route
from flightplan import FlightPlan
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


def compare_optimal_paths(path_1: FlightPlan, path_2: FlightPlan):

    # equal choose money over distance or sm
    if path_1.ratio > path_2.ratio:
        # Compare path ratios
        return path_1
    elif path_1.ratio == path_2.ratio:
        # Equal path ratios, return path with smaller distance travelled
        if path_1.distance_travelled < path_2.distance_travelled:
            return path_1

    return path_2


def calculate_optimized_path(current_waypoint: Waypoint, routes: list[Waypoint], final_waypoints: list[Waypoint], acc_time: float) -> FlightPlan:
    if not routes:
        # No other starting points left
        return 0, 0, []
    elif len(routes) == 1:
        
        if routes[0].start_waypoint == current_waypoint:
            # 1 Route left, you are at starting position, complete route
            flightplan = FlightPlan(routes[0].reward, routes[0].distance)
            # Add path to return to origin
            flightplan.add_route_tail(routes[0].end_waypoint, final_waypoints[0])
            flightplan.return_route()
            return flightplan
        else:
            # Not at the starting waypoint as the last route
            flightplan = FlightPlan(routes[0].reward, routes[0].distance)
            # Route added to start of planned route
            flightplan.add_route_tail(current_waypoint, routes[0].start_waypoint, withoutStart=True)
            # Add path to return to origin
            flightplan.add_route_tail(routes[0].end_waypoint, final_waypoints[0])
            flightplan.return_route()

            return flightplan

    else:
        next_possible_wp = get_next_waypoint(current_waypoint, routes)

        calculated_optimized_next = {}
        
        for next_wp, route_index, at_start_wp in next_possible_wp:
        
            if at_start_wp:
                # Doing the route
                route_completed = routes.pop(route_index)
                acc_time_update = acc_time + route_completed.distance / FlightPlan.drone_speed
                if FlightPlan.max_time_in_flight < acc_time:
                    routes.insert(route_index, route_completed)
                    continue
                flightplan = calculate_optimized_path(next_wp, routes, final_waypoints + [current_waypoint], acc_time_update)
                # Complete Route
                flightplan.complete_route()
                routes.insert(route_index, route_completed)
            else:
                max_wp_threshold = 2
                if count_waypoint_occurances(next_wp, final_waypoints) < max_wp_threshold:
                    # If waypoint has not been passed more than twice, go to waypoint (configurable)
                    route_completed = Route(-1, 0, current_waypoint.name, next_wp.name, 99999, "", 0)
                    acc_time_update = acc_time + route_completed.distance / FlightPlan.drone_speed
                    if FlightPlan.max_time_in_flight < acc_time:
                        continue
                    flightplan = calculate_optimized_path(next_wp, routes, final_waypoints + [current_waypoint], acc_time_update)
                else:
                    # skip next_wp option if it has been passed more than twice
                    continue

            flightplan.calculate_ratio()
            flightplan.add_route_head(route_completed.reward,
                                  route_completed.distance,
                                  next_wp)

            if flightplan.is_low_battery():
                continue
            
            if next_wp.name in calculated_optimized_next:
                calculated_optimized_next[next_wp.name] = compare_optimal_paths(calculated_optimized_next[next_wp.name],
                                                                                flightplan)
            else:
                calculated_optimized_next[next_wp.name] = flightplan

        # reward, distance, ratio, waypoints
        best_path = FlightPlan(-1, 99999, [])
        best_path.calculate_ratio()

        for name in calculated_optimized_next:
            reward_distance_values = calculated_optimized_next[name]
            best_path = compare_optimal_paths(best_path, reward_distance_values)

        return best_path


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

    flightplan = calculate_optimized_path(start_wp, all_routes, [start_wp], 0)
    flightplan.waypoints = [start_wp] + flightplan.waypoints
    
    print(flightplan.time_accumulated)
    return flightplan.waypoints

if __name__ == "__main__":
    # sys.setrecursionlimit(5000)
    stuff = task_2()
    print(stuff)
