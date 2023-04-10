from random import randint
from waypoint import WAYPOINT_LST, Waypoint, ALL_WAYPOINTS
from route import Route

def generate_routes(num_routes : int) -> list[Route]:
    final_routes = []
    all_wp_copy = ALL_WAYPOINTS.copy()
    counter = 1

    while len(final_routes) < num_routes:
        # Generate starting waypoint
        i = randint(1,len(all_wp_copy) - 1)
        start_wp = all_wp_copy[i]

        # Store start wp chosen
        all_wp_copy.pop(i)
        
        # Generate end waypoint
        i = randint(1,len(all_wp_copy) - 1)
        end_wp = all_wp_copy[i]

        # Store end wp chosen
        all_wp_copy.pop(i)

        new_route = Route(counter, 6, start_wp.name, end_wp.name, 10, "", randint(1,500))
        counter += 1

        final_routes.append(new_route)

    return final_routes
