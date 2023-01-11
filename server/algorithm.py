from waypoint import WAYPOINT_LST, Waypoint
from route import Route
from flightplan import FlightPlan


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


def calculate_optimized_path(current_waypoint: Waypoint, routes: list[Waypoint], final_waypoints: list[Waypoint],
                             acc_time: float) -> FlightPlan:
    if not routes:
        # No other starting points left
        return FlightPlan()

    elif len(routes) == 1:

        if routes[0].start_waypoint == current_waypoint:
            # 1 Route left, you are at starting position, complete route
            flightplan = FlightPlan(routes[0].reward, routes[0].distance)

            # Verify that there is enough battery to complete the final route
            acc_time_update = acc_time + flightplan.time_accumulated + FlightPlan.time_to_land
            if acc_time_update > FlightPlan.max_time_on_battery:
                flightplan.append_at_next_head()

            # Add path to return to origin
            flightplan.add_route_tail_wp_only(routes[0].end_waypoint, final_waypoints[0])
            return flightplan
        else:
            # Not at the starting waypoint as the last route
            flightplan = FlightPlan(routes[0].reward, routes[0].distance)
            # Route added to start of planned route
            flightplan.add_route_tail(current_waypoint, routes[0].start_waypoint, without_start=True)

            # Verify if there is enough battery to travel to start of planned route and complete
            acc_time_update = acc_time + flightplan.time_accumulated + FlightPlan.time_to_land
            if acc_time_update > FlightPlan.max_time_on_battery:
                flightplan.battery_swap()
            # Add path to return to origin
            flightplan.add_route_tail_wp_only(routes[0].end_waypoint, final_waypoints[0])

            return flightplan

    else:
        next_possible_wp = get_next_waypoint(current_waypoint, routes)

        calculated_optimized_next = {}
        # Signal to add a stop at origin before current waypoint
        add_origin_before_route_head = False

        for next_wp, route_index, at_start_wp in next_possible_wp:

            if at_start_wp:
                # Doing the route
                route_completed = routes.pop(route_index)
                acc_time_update = acc_time + (
                        route_completed.distance / FlightPlan.drone_speed) + FlightPlan.time_to_land + \
                    FlightPlan.time_to_load + FlightPlan.time_to_takeoff

                if FlightPlan.is_low_battery(acc_time, route_completed.distance, next_wp):
                    # route will need more battery life, signal to go back to origin
                    # prior to starting route 
                    add_origin_before_route_head = True
                    # reset time accumulated to start with this route only + time from origin to start (s)
                    acc_time_update = acc_time_update - acc_time + FlightPlan.get_time_from_origin(current_waypoint)

                flightplan = calculate_optimized_path(next_wp, routes, final_waypoints + [current_waypoint],
                                                      acc_time_update)
                flightplan.complete_route()
                routes.insert(route_index, route_completed)
            else:
                max_wp_threshold = 2
                if count_waypoint_occurances(next_wp, final_waypoints) < max_wp_threshold:
                    # If waypoint has not been passed more than twice, go to waypoint (configurable)
                    route_completed = Route(-1, 0, current_waypoint.name, next_wp.name, 99999, "", 0)
                    # Current accumulated time plus time to next waypoint
                    acc_time_update = acc_time + route_completed.distance / FlightPlan.drone_speed

                    if FlightPlan.is_low_battery(acc_time, route_completed.distance, next_wp):
                        # route will need more battery life, add a stop at origin before
                        # going to next_wp

                        # reset time to time taken from refuel to next waypoint
                        acc_time_update = FlightPlan.get_time_from_origin(next_wp)
                        flightplan = calculate_optimized_path(next_wp, routes, final_waypoints + [current_waypoint],
                                                              acc_time_update)
                        # Add signal such that next time a wp is added to the head, origin is added as well
                        flightplan.append_at_next_head()
                    else:
                        flightplan = calculate_optimized_path(next_wp, routes, final_waypoints + [current_waypoint],
                                                              acc_time_update)
                else:
                    # skip next_wp option if it has been passed more than twice
                    continue

            flightplan.calculate_ratio()
            flightplan.add_route_head(route_completed.reward,
                                      route_completed.distance,
                                      next_wp)

            if add_origin_before_route_head:
                # Check for signal to add origin before route
                add_origin_before_route_head = False
                # Signal for flightplan to add origin before whichever wp is added to the head next
                flightplan.append_at_next_head()

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
    r_1 = Route(1, 2, "Lima", "Quebec", 15, "Obstacle", 112.0)
    r_2 = Route(2, 6, "Delta", "Charlie", 5, "nil", 50.0)
    r_3 = Route(3, 4, "Alpha", "Zulu", 15, "Comment", 150.0)
    all_routes = [r_1, r_2, r_3]

    flightplan = calculate_optimized_path(start_wp, all_routes, [start_wp], FlightPlan.time_to_takeoff)
    flightplan.waypoints = [start_wp] + flightplan.waypoints
    flightplan.takeoff()

    print(flightplan.time_accumulated)
    return flightplan.waypoints


if __name__ == "__main__":
    # sys.setrecursionlimit(5000)
    stuff = task_2()
    print(stuff)
