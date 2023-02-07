

def calc_min_req_velocity(num_stops: int, stop_time: float, total_dist: float, allowed_time: float) -> float:
    """Given a number of stops, the time taken at each stop, the total distance required to travel and a max time
    return the minimum velocity needed to complete the route in the allowed time

    :param num_stops: number of stops required along route (int)
    :param stop_time: time required at each stop - seconds (float)
    :param total_dist: total distance travelled during the route - meters (float)
    :param allowed_time: max time allowed to complete distance with stops - seconds (float)
    :return minimum drone airspeed to complet
    """
    
    time_taken_from_stops = num_stops * stop_time

    return total_dist / (allowed_time - time_taken_from_stops)
    

if __name__ == '__main__':
    res = calc_min_req_velocity(4, 150.0, 14032.708919289533, 7200)
    print(res)