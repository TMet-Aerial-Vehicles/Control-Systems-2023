from waypoint import Waypoint
from utils import calculate_distance

class FlightPlan:
    # Tunable Parameters
    drone_speed = 1 # metres / seconds
    time_to_takeoff = 60 # seconds
    time_to_land = 80 # seconds
    time_to_load = 10 # seconds

    def __init__(self, reward: float, distance: float, waypoints: list = []) -> None:
        self.reward_collected = reward
        self.distance_travelled = distance
        self.waypoints = waypoints
        self.time_accumulated = 0
        self.ratio = 0

    def calculate_ratio(self) -> None:
        if self.distance_travelled == 0:
            self.ratio = 0
        else:
            self.ratio = self.reward_collected / self.distance_travelled

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