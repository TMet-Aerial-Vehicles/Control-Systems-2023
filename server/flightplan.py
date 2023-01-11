from waypoint import WAYPOINT_LST, Waypoint
from utils import calculate_distance

class FlightPlan:
    # Tunable Parameters
    drone_speed = 10.0 # metres / seconds
    time_to_takeoff = 60.0 # seconds
    time_to_land = 80.0 # seconds
    time_to_load = 10.0 # seconds
    max_time_on_battery = 1200.0 # seconds

    def __init__(self, reward: float = 0.0, distance: float = 0.0, waypoints: list = []) -> None:
        self.reward_collected = reward
        self.distance_travelled = distance
        self.waypoints = waypoints
        self.time_accumulated = self.distance_travelled / self.drone_speed
        self.ratio = 0
        self.origin_head = None
        self.acc_time = 0.0
    def calculate_ratio_reward_dist(self) -> None:
        if self.distance_travelled == 0.0:
            self.ratio = 0
        else:
            self.ratio = self.reward_collected / self.distance_travelled

    def calculate_ratio(self) -> None:
        # Maximize reward, minimize time and distance
        if (self.distance_travelled * self.time_accumulated) == 0.0:
            self.ratio = 0
        else:
            self.ratio = self.reward_collected / (self.distance_travelled * self.time_accumulated)

    def add_route_tail_wp_only(self, start_wp: Waypoint, end_wp: Waypoint) -> None:
        self.waypoints = self.waypoints + [start_wp, end_wp]

    def add_route_tail(self, start_wp: Waypoint, end_wp: Waypoint, reward: int = None, withoutStart: bool = False):
        dist = calculate_distance(start_wp, end_wp)
        self.distance_travelled += dist
        self.update_time(dist / self.drone_speed)

        if withoutStart:
            self.waypoints = self.waypoints + [end_wp]
        else:
            self.waypoints = self.waypoints + [start_wp, end_wp]

        if reward:
            self.reward_collected += reward

    def add_route_head(self, reward: float, distance: int, waypoint: Waypoint):
        self.distance_travelled += distance
        self.update_time(distance / self.drone_speed)
        self.waypoints = [waypoint] + self.waypoints
        self.reward_collected += reward

        if self.origin_head:
            self.origin_head = None
            self.battery_swap()

    def takeoff(self) -> None:
        self.update_time(self.time_to_takeoff)

    def land(self) -> None:
        self.update_time(self.time_to_land)

    def load(self) -> None:
        self.update_time(self.time_to_load)

    def update_time(self, add_time: float) -> None:
        self.time_accumulated += add_time

    def complete_route(self) -> None:
        self.land()
        self.load()
        self.takeoff()
    
    def append_at_next_head(self) -> None:
        self.origin_head = WAYPOINT_LST.get_wp_by_name("Origin")

    def is_low_battery(acc_time: float, est_distance: float, next_wp: Waypoint) -> bool:
        origin = WAYPOINT_LST.get_wp_by_name("Origin")
        dist_to_origin = calculate_distance(next_wp, origin)

        time_to_next_wp = est_distance / FlightPlan.drone_speed
        time_to_origin_from_next_wp = dist_to_origin / FlightPlan.drone_speed

        # Calculate time to next wp, then to origin including land, load, takeoff
        acc_time_update = acc_time + time_to_next_wp + FlightPlan.time_to_land \
            + FlightPlan.time_to_load + FlightPlan.time_to_takeoff + time_to_origin_from_next_wp
        
        # Determine if going to next waypoint and then to origin will take more battery then currently have
        return acc_time_update > FlightPlan.max_time_on_battery 

    def get_time_from_origin(next_wp: Waypoint) -> float:
        origin = WAYPOINT_LST.get_wp_by_name("Origin")
        return calculate_distance(origin, next_wp) / FlightPlan.drone_speed

    def battery_swap(self) -> None:
        origin = WAYPOINT_LST.get_wp_by_name("Origin")
        dist_to_origin = calculate_distance(self.waypoints[0], origin)
        self.add_route_head(0.0, dist_to_origin, origin)