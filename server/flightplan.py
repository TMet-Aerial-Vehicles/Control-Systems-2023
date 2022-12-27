from waypoint import Waypoint
from utils import calculate_distance

class FlightPlan:
    # Tunable Parameters
    drone_speed = 1.0 # metres / seconds
    time_to_takeoff = 60.0 # seconds
    time_to_land = 80.0 # seconds
    time_to_load = 10.0 # seconds
    max_time_in_flight = 12000.0 # seconds

    def __init__(self, reward: float = 0.0, distance: float = 0.0, waypoints: list = []) -> None:
        self.reward_collected = reward
        self.distance_travelled = distance
        self.waypoints = waypoints
        self.time_accumulated = 0.0
        self.ratio = 0
        # Flight plan always start with takeoff
        self.takeoff()

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

    def add_route_tail(self, start_wp: Waypoint, end_wp: Waypoint, reward: int = None, withoutStart: bool = False):
        dist = calculate_distance(start_wp, end_wp)
        self.distance_travelled += dist
        self.time_accumulated += dist / self.drone_speed

        if withoutStart:
            self.waypoints = self.waypoints + [end_wp]
        else:
            self.waypoints = self.waypoints + [start_wp, end_wp]

        if reward:
            self.reward_collected += reward

    def add_route_head(self, reward: float, distance: int, waypoint: Waypoint):
        self.distance_travelled += distance
        self.time_accumulated += (distance / self.drone_speed)
        self.waypoints = [waypoint] + self.waypoints
        self.reward_collected += reward

    def takeoff(self) -> None:
        self.time_accumulated += self.time_to_takeoff

    def land(self) -> None:
        self.time_accumulated += self.time_to_land

    def load(self) -> None:
        self.time_accumulated += self.time_to_load

    def complete_route(self) -> None:
        self.land()
        self.load()
        self.takeoff()
    
    def return_route(self) -> None:
        self.takeoff()
        self.land()

    def is_low_battery(self) -> bool:
        return self.time_accumulated > self.max_time_in_flight