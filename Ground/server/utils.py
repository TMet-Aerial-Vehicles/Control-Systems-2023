# Common Method File

import os

from geopy import distance
from waypoint import Waypoint


PROJECT_NAME = "Control-Systems-2023"


def get_root_dir() -> str:
    """Returns a path to the project root directory, checking max 3 parent dirs

    :return: (str) Path to project root folder
    """
    cwd = os.getcwd()

    max_iterations = 3
    iter_count = 0
    while iter_count < max_iterations:
        if cwd.endswith(PROJECT_NAME):
            return cwd
        else:
            cwd = os.path.dirname(cwd)
            iter_count += 1
    return os.getcwd()


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
