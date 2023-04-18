import os
import configparser
import math

import sys
sys.path.append('../../')


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))


def get_root_dir() -> str:
    """Returns a path to the project root directory, checking max 3 parent dirs

    :return: (str) Path to project root folder
    """
    cwd = os.getcwd()
    max_iterations = 5
    iter_count = 0
    while iter_count < max_iterations:
        if cwd.endswith(config["Shared"]["Project_Name"]):
            return cwd
        else:
            cwd = os.path.dirname(cwd)
            iter_count += 1
    return os.getcwd()


def error_dict(message) -> dict:
    """Create Dict with success False and error message

    :param message: Message to return with (str)
    :return: Dictionary with success False and response message
    """
    return {
        "success": False,
        "message": message
    }


def success_dict(message) -> dict:
    """Create Dict with success True and success message

    :param message: Message to return with (str)
    :return: Dictionary with success True and response message
    """
    return {
        "success": True,
        "message": message
    }


def get_distance_meters(lat1, lon1, lat2, lon2):
    """Returns the north and east offset in meters between two pairs of
    latitude and longitude coordinates."""

    # Earth radius in meters
    earth_radius = 6371000

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Calculate the difference between the two longitude values
    dlon = lon2 - lon1

    # Calculate the difference between the two latitude values
    dlat = lat2 - lat1

    # Calculate the haversine of half the difference in latitude
    a = math.sin(dlat / 2) ** 2

    # Calculate the haversine of half the difference in longitude
    b = math.sin(dlon / 2) ** 2

    # Calculate the haversine of the latitude values
    c = math.cos(lat1) * math.cos(lat2)

    # Calculate the central angle between the two coordinates
    central_angle = 2 * math.asin(math.sqrt(a + c * b))

    # Calculate the distance in meters
    distance = earth_radius * central_angle

    # Calculate the north and east offsets
    north_offset = distance * math.cos(math.atan2(dlat, dlon))
    east_offset = distance * math.sin(math.atan2(dlat, dlon))

    return north_offset, east_offset
