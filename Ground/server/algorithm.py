from waypoint import WAYPOINT_LST, Waypoint
from route import Route
from flightplan import FlightPlan
from route_generator import generate_routes
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../..', 'config.ini'))

def format_for_execute_command(flightplan: FlightPlan) -> list:
    command_sequence = []
    for i in range(len(flightplan.waypoints)):
        curr_wp = flightplan.waypoints[i]
        instruction = flightplan.instructions[i]
# --------------------------------------- TAKEOFF ---------------------------------------
        if instruction == "Takeoff":
            cmd = {
                "Command" : "Takeoff",
                "Details" : {"Altitude" : config["Ground"]["ALTITUDE"]}
            }
            command_sequence.append(cmd)

# --------------------------------------- RTL-CR ---------------------------------------
        elif instruction == "RTL-CR":
            # need to [land, load, battery swap, takeoff]
            # Navigate to Waypoint
            cmd = {
                "Command" : "Navigate",
                "Details" : {
                    "Name" : curr_wp.name,
                    "Latitude" : curr_wp.latitude,
                    "Longitude" : curr_wp.longitude,
                    "Altitude" : config["Ground"]["ALTITUDE"]
                }
            }
            command_sequence.append(cmd)

            # Land Command
            cmd = {
                "Command" : "Land"
            }
            command_sequence.append(cmd)

            # Hold Command
            cmd = {
                "Command" : "Hold",
                "Details" : {"Time" : FlightPlan.time_to_load}
            }
            command_sequence.append(cmd)

            # Battery Swap Command
            cmd = {
                "Command" : "BatterySwap"
            }
            command_sequence.append(cmd)

            # Takeoff command
            cmd = {
                "Command" : "Takeoff",
                "Details" : {"Altitude" : config["Ground"]["ALTITUDE"]}
            }
            command_sequence.append(cmd)

# --------------------------------------- RTL-BSWP ---------------------------------------
        elif instruction == "RTL-BSWP":
            # need to [land, battery swap, takeoff]
            # Navigate to Waypoint
            cmd = {
                "Command" : "Navigate",
                "Details" : {
                    "Name" : curr_wp.name,
                    "Latitude" : curr_wp.latitude,
                    "Longitude" : curr_wp.longitude,
                    "Altitude" : config["Ground"]["ALTITUDE"]
                }
            }
            command_sequence.append(cmd)

            # Land Command
            cmd = {
                "Command" : "Land"
            }
            command_sequence.append(cmd)

            # Battery Swap Command
            cmd = {
                "Command" : "BatterySwap"
            }
            command_sequence.append(cmd)

            # Takeoff command
            cmd = {
                "Command" : "Takeoff",
                "Details" : {"Altitude" : config["Ground"]["ALTITUDE"]}
            }
            command_sequence.append(cmd)
# --------------------------------------- END / START ---------------------------------------
        elif instruction == "END" or instruction == "START":
            # Navigate to Waypoint need to [land, load, takeoff]
            cmd = {
                "Command" : "Navigate",
                "Details" : {
                    "Name" : curr_wp.name,
                    "Latitude" : curr_wp.latitude,
                    "Longitude" : curr_wp.longitude,
                    "Altitude" : config["Ground"]["ALTITUDE"]
                }
            }
            command_sequence.append(cmd)

            # Land Command
            cmd = {
                "Command" : "Land"
            }
            command_sequence.append(cmd)

            # Hold Command
            cmd = {
                "Command" : "Hold",
                "Details" : {"Time" : FlightPlan.time_to_load}
            }
            command_sequence.append(cmd)

            # Takeoff command
            cmd = {
                "Command" : "Takeoff",
                "Details" : {"Altitude" : config["Ground"]["ALTITUDE"]}
            }
            command_sequence.append(cmd)

# --------------------------------------- START-I0 ---------------------------------------
        elif instruction == "START-I0":
            # Hold Command
            cmd = {
                "Command" : "Hold",
                "Details" : {"Time" : FlightPlan.time_to_load}
            }
            command_sequence.append(cmd)

            # Takeoff command
            cmd = {
                "Command" : "Takeoff",
                "Details" : {"Altitude" : config["Ground"]["ALTITUDE"]}
            }
            command_sequence.append(cmd)

    return command_sequence[:-2]

def is_route(start_wp: Waypoint, end_wp: Waypoint, routes: list[Route]) -> tuple[bool, int]:
    for route in routes:
        if route.start_waypoint == start_wp and route.end_waypoint == end_wp:
            return True, route.number
    return False, -1

def add_route_instructions(waypoints: list[Waypoint], routes: list[Route], battery_swaps : list[int]) -> tuple[list, list]:
    """Build route instructions using the generated waypoint list. RTL = Return to Starting Point
    [Land, Load, Takeoff] = Route Completion Process after Navigating to WP
    FLY = Only navigate to the WP

    param waypoints: current waypoint in route path ([Waypoint])
    param routes: routes provided by competition ([Route])
    :return: list containing instructions for each waypoint, list specifying route completion 
    order (using route num)
    """
    check_route, route_num = is_route(waypoints[0], waypoints[1], routes)
    if check_route:
        instructions = ["START-I0"]
    else:
        instructions = ["Takeoff"]
    route_plan = []
    i = 1
    
    while i < len(waypoints):
        check_route, route_num = is_route(waypoints[i - 1], waypoints[i], routes)
        if (waypoints[i].name == FlightPlan.origin.name) and (i in battery_swaps):
            if check_route:
                # Complete route and battery swap
                route_plan.append(route_num)
                instructions.extend(["RTL-CR"]) # need to [land, load, battery swap, takeoff]
            else:
                instructions.extend(["RTL-BSWP"]) # need to [land, battery swap, takeoff]
        elif check_route:
            # Is a route END
            route_plan.append(route_num)
            instructions.extend(["END"]) # need to [land, load, takeoff]
        else:
            # Is a route START
            instructions.extend(["START"]) # need to [land, load, takeoff]

        i += 1
    return instructions, route_plan

def count_waypoint_occurances(curr_wp: Waypoint, final_waypoints: list[Waypoint]) -> int:
    """Recursive algorithm which builds a route path through all desired waypoints using provided routes
    and time / distance / reward considerations.

    param curr_wp: current waypoint in route path (Waypoint)
    param final_waypoints: waypoints traversed as a flight plan is built ([Waypoint])
    :return: number of occurances of a waypoint in the complete waypoint list
    """
    if curr_wp is None:
        return 0
    
    return len([wp for wp in final_waypoints if wp.name == curr_wp.name])


def get_next_waypoint_opts(current_waypoint: Waypoint, routes: list[Route]) -> tuple[list, float]:
    """Build a list of next waypoint options based on the current waypoint and the list of routes
    remaining to be completed.

    param current_waypoint: current waypoint in route path (Waypoint)
    param routes: list of routes provided to be completed in final flight plan ([Waypoint])
    :return: 1. list of next waypoint options containing the next waypoint, index in routes and bool
    depicting if the completing a route or not [(Waypoint, int, bool)]. 2. min time to next waypoint (float)
    """    
    next_possible_waypoints = []
    max_dist_to_nextwp = 10000
    for i_route in range(len(routes)):
        if routes[i_route].start_waypoint == current_waypoint:
            next_possible_waypoints.append((routes[i_route].end_waypoint, i_route, True))
            max_dist_to_nextwp = max(max_dist_to_nextwp, FlightPlan.calculate_distance(current_waypoint, routes[i_route].end_waypoint))
        else:
            next_possible_waypoints.append((routes[i_route].start_waypoint, i_route, False))
            max_dist_to_nextwp = max(max_dist_to_nextwp, FlightPlan.calculate_distance(current_waypoint, routes[i_route].start_waypoint))

    return next_possible_waypoints, max_dist_to_nextwp / FlightPlan.drone_speed

def compare_optimal_paths(path_1: FlightPlan, path_2: FlightPlan) -> FlightPlan:
    """Compare the pre-computed ratio between two FlightPlan's, returning the best option

    param path_1: Flight plan option with computed ratio (FlightPlan)
    param path_2: Flight plan option with computed ratio (FlightPlan)
    :return: FlightPlan with route plan and route specific details (FlightPlan)
    """
    # equal choose money over distance or sm
    if path_1.ratio > path_2.ratio:
        # Compare path ratios
        return path_1
    elif path_1.ratio == path_2.ratio:
        # Equal path ratios, return path with smaller distance travelled
        if path_1.distance_travelled < path_2.distance_travelled:
            return path_1

    return path_2


def calculate_optimized_path(current_waypoint: Waypoint, routes: list[Route], final_waypoints: list[Waypoint],
                             acc_time: float, total_time: float) -> FlightPlan:
    """Recursive algorithm which builds a route path through all desired waypoints using provided routes
    and time / distance / reward considerations.

    param current_waypoint: current waypoint in route path (Waypoint)
    param routes: list of routes provided to be completed in final flight plan ([Waypoint])
    param final_waypoints: waypoints traversed as a flight plan is built ([Waypoint])
    param acc_time: time accumulated as routes are completed (float)
    :return: FlightPlan with route plan and route specific details
    """

    # Extract data from next_wp_predict
    next_possible_wp, max_possible_next_time = get_next_waypoint_opts(current_waypoint, routes)

    if (total_time + max_possible_next_time) >= FlightPlan.max_time_in_air:
        # Max time in air reached
        return FlightPlan(waypoints=[FlightPlan.origin])

    elif len(routes) == 1:

        if routes[0].start_waypoint == current_waypoint:
            # 1 Route left, you are at starting position, complete route
            flightplan = FlightPlan(routes[0].reward, routes[0].distance)

            # Verify that there is enough battery to complete the final route
            acc_time_update = acc_time + flightplan.time_accumulated + 2 * (FlightPlan.time_to_land \
                + FlightPlan.time_to_load) + FlightPlan.time_to_takeoff
            if acc_time_update > FlightPlan.max_time_on_battery:
                flightplan.append_at_next_head()
                acc_time_update += FlightPlan.time_to_swap_battery

            # Add path to return to origin
            flightplan.add_route_tail_wp_only(routes[0].end_waypoint, final_waypoints[0])

            # start procedure
            flightplan.complete_route()
            # end procedure
            flightplan.complete_route()
            
            return flightplan
        else:
            # Not at the starting waypoint as the last route
            flightplan = FlightPlan(routes[0].reward, routes[0].distance)
            # Route added to start of planned route
            flightplan.add_route_tail(current_waypoint, routes[0].start_waypoint, without_start=True)

            # Verify if there is enough battery to travel to start of planned route and complete
            acc_time_update = acc_time + flightplan.time_accumulated + 2 * (FlightPlan.time_to_land \
                + FlightPlan.time_to_load) + FlightPlan.time_to_takeoff
            if acc_time_update > FlightPlan.max_time_on_battery:
                flightplan.battery_swap()
                acc_time_update += FlightPlan.time_to_swap_battery
            # Add path to return to origin
            flightplan.add_route_tail_wp_only(routes[0].end_waypoint, final_waypoints[0])

            # start procedure
            flightplan.complete_route()
            # end procedure
            flightplan.complete_route()
            
            return flightplan

    else:

        route_opt = (-1, False) # route_index, is_completing_route
        min_ratio = 10000 # ratio = dist / reward
        for next_wp, route_index, at_start_wp in next_possible_wp:
            route = routes[route_index]
            ratio_cr = 10000
            ratio_ncr = 10000
            
            if at_start_wp:
                # next_wp could complete a route
                ratio_cr = route.distance / route.reward

            else:
                # next_wp is the begining of another route
                dist = FlightPlan.calculate_distance(current_waypoint, next_wp)
                ratio_ncr = (dist + route.distance) / route.reward

            if ratio_cr <= min_ratio:
                min_ratio = ratio_cr
                route_opt = (route_index, True)
            if ratio_ncr < min_ratio:
                min_ratio = ratio_ncr
                route_opt = (route_index, False)

        route_index, complete_route = route_opt

        # Signal to add a stop at origin before current waypoint
        add_origin_before_route_head = False

        if(complete_route):
            # Doing the route current_wp = start, next_wp = end
            route_completed = routes.pop(route_index)
            next_wp = route_completed.end_waypoint
            rtl_swap = False

            acc_time_update = acc_time + (
                    route_completed.distance / FlightPlan.drone_speed) + 2 * (FlightPlan.time_to_land + \
                FlightPlan.time_to_load + FlightPlan.time_to_takeoff)
            total_time_update = total_time + acc_time_update - acc_time

            if FlightPlan.is_low_battery(acc_time, route_completed.distance, next_wp) or FlightPlan.rtl_swap_battery(current_waypoint, acc_time_update):
                # route will need more battery life, signal to go back to origin
                # prior to starting route 
                add_origin_before_route_head = True
                # reset time accumulated to start with this route only + time from origin to start (s)
                acc_time_update = acc_time_update - acc_time + FlightPlan.get_time_from_origin(current_waypoint) + FlightPlan.time_to_takeoff
                total_time_update += FlightPlan.get_time_from_origin(current_waypoint) + FlightPlan.time_to_swap_battery + FlightPlan.time_to_takeoff

            elif FlightPlan.rtl_swap_battery(next_wp, acc_time_update):
                acc_time_update = FlightPlan.time_to_takeoff
                total_time_update += FlightPlan.time_to_swap_battery + FlightPlan.time_to_takeoff
                rtl_swap = True

            flightplan = calculate_optimized_path(next_wp, routes, final_waypoints + [current_waypoint],
                                                acc_time_update, total_time_update)
            
            # pickup procedure
            flightplan.complete_route()
            # drop off procedure
            flightplan.complete_route()

            if rtl_swap:
                flightplan.append_at_next_head()

            flightplan.add_route_head(route_completed.reward,
                            route_completed.distance,
                            next_wp)

            if add_origin_before_route_head:
                # Check for signal to add origin before route
                add_origin_before_route_head = False
                # Signal for flightplan to add origin before whichever wp is added to the head next
                flightplan.append_at_next_head()
            
            return flightplan

        else:
            # Not Completing Route, Move to next best starting point for a route (assume in air)
            route_to_complete = routes[route_index]
            next_wp = route_to_complete.start_waypoint
            route_completed = Route(-1, 0, current_waypoint.name, next_wp.name, 99999, "", 0)
            
            # Current accumulated time plus time to next waypoint
            acc_time_update = acc_time + route_completed.distance / FlightPlan.drone_speed
            total_time_update = total_time + route_completed.distance / FlightPlan.drone_speed

            if FlightPlan.is_low_battery(acc_time, route_completed.distance, next_wp) or FlightPlan.rtl_swap_battery(next_wp, acc_time_update):
                # route will need more battery life, add a stop at origin before
                # going to next_wp

                # reset time to time taken from refuel to next waypoint
                acc_time_update = FlightPlan.get_time_from_origin(next_wp) + FlightPlan.time_to_takeoff
                total_time_update -= route_completed.distance / FlightPlan.drone_speed
                total_time_update += acc_time_update + FlightPlan.get_time_from_origin(current_waypoint) + FlightPlan.time_to_swap_battery \
                    + FlightPlan.time_to_takeoff
                flightplan = calculate_optimized_path(next_wp, routes, final_waypoints + [current_waypoint],
                                                        acc_time_update, total_time_update)
                # Add signal such that next time a wp is added to the head, origin is added as well
                flightplan.append_at_next_head()
            else:
                flightplan = calculate_optimized_path(next_wp, routes, final_waypoints + [current_waypoint],
                                                        acc_time_update, total_time_update)
            
            flightplan.add_route_head(route_completed.reward,
                                    route_completed.distance,
                                    next_wp)
            
            return flightplan 


def task_2(all_routes: list[Route]) -> FlightPlan:
    """Recursive algorithm which builds a route path through all desired waypoints using provided routes
    and time / distance / reward considerations.

    param routes: list of routes provided to be completed in final flight plan ([Waypoint])
    :return: FlightPlan with route plan and route specific details
    """
    start_wp = FlightPlan.origin

    flightplan = calculate_optimized_path(start_wp, all_routes.copy(), [], FlightPlan.time_to_takeoff, FlightPlan.time_to_takeoff)
    flightplan.waypoints = [start_wp] + flightplan.waypoints
    flightplan.takeoff()

    flightplan.reformat_battery_indexes()

    flightplan.instructions, flightplan.route_plan = add_route_instructions(flightplan.waypoints, all_routes, flightplan.battery_swap_indexes)

    return flightplan


if __name__ == "__main__":
    r_1 = Route(1, 2, "Lima", "Quebec", 15, "Obstacle", 412.0)
    r_2 = Route(2, 6, "Delta", "Charlie", 5, "nil", 50.0)
    r_3 = Route(3, 4, "Alpha", "Zulu", 15, "Comment", 150.0)
    r_4 = Route(4, 1, "Charlie", "Golf", 10, "", 70.0)
    r_5 = Route(5, 1, "November", "Xray", 10, "", 200.0)
    r_6 = Route(6, 1, "Echo", "Hotel", 10, "", 243.0)
    r_7 = Route(7, 1, "Bravo", "Golf", 10, "", 43.0)
    # all_routes = [r_1,r_2,r_3,r_4,r_5,r_6,r_7]
    all_routes = generate_routes(8)
    print("--------- ROUTES ----------")
    print(all_routes)
    flightplan = task_2(all_routes)
    print("------- FLIGHTPLAN --------")
    print(flightplan.waypoints)
    print(flightplan.battery_swap_indexes)
    print(flightplan.time_accumulated)

    # for i in range(len(flightplan.waypoints)):
    #     print(flightplan.waypoints[i].name + " --> " + str(flightplan.instructions[i]))

    print(flightplan.generate_email()["Body"])
    commands = format_for_execute_command(flightplan)
    for command in commands: print(command)

