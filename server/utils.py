# Common Method File
from geopy import distance
from waypoint import Waypoint


def calculate_distance(start_wp: Waypoint, end_wp: Waypoint) -> float:
    """Returns the distance in metres between two Waypoint objects.

    :param start_wp:
    :param end_wp:
    :return:
    """
    return distance.distance(
        (start_wp.latitude, start_wp.longitude),
        (end_wp.latitude, end_wp.longitude)
    ).meters


def calculate_circle_distance(start_wp: Waypoint, end_wp: Waypoint) -> float:
    """Returns the distance in metres between two Waypoint objects.

    :param start_wp:
    :param end_wp:
    :return:
    """
    return distance.great_circle(
        (start_wp.latitude, start_wp.longitude),
        (end_wp.latitude, end_wp.longitude)
    ).meters

def calculate_geodesic(start_wp: Waypoint, end_wp: Waypoint) -> float:
    """Returns the distance in metres between two Waypoint objects.

    :param start_wp:
    :param end_wp:
    :return:
    """
    return distance.geodesic(
        (start_wp.latitude, start_wp.longitude),
        (end_wp.latitude, end_wp.longitude)
    ).meters
