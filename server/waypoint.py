from typing import Union


class Waypoint:
    def __init__(self, name, number, longitude, latitude):
        """Initialize Waypoint object

        :param name: Waypoint name to associate with (str)
        :param number: Waypoint unique number (int)
        :param longitude: Longitude coordinate of Waypoint (float)
        :param latitude: Latitude coordinate of Waypoint (float)
        """
        self.name = name
        self.number = number
        self.longitude = longitude
        self.latitude = latitude

    def to_dict(self):
        """Converts Waypoint object to dictionary

        :return: Dictionary with Waypoint details
        """
        return {
            "name": self.name,
            "number": self.number,
            "latitude": self.latitude,
            "longitude": self.longitude
        }


ALL_WAYPOINTS = [
    Waypoint("Alpha", 1, -71.6375025, 48.5166707),
    Waypoint("Bravo", 2, -71.6317518, 48.5060947),
    Waypoint("Charlie", 3, -71.6340069, 48.4921159),
    Waypoint("Delta", 4, -71.6404442, 48.5150341),
    Waypoint("Echo", 5, -71.6782955, 48.5005337),
    Waypoint("Foxtrot", 6, -71.6040591, 48.5088395),
    Waypoint("Golf", 7, -71.6522101, 48.5101473),
    Waypoint("Hotel", 8, -71.6426006, 48.5129917),
    Waypoint("India", 9, -71.6428152, 48.5117408),
    Waypoint("Juliette", 10, -71.6229056, 48.5193311),
    Waypoint("Kilo", 11, -71.6568088, 48.4984623),
    Waypoint("Lima", 12, -71.6253089, 48.5019885),
    Waypoint("Mike", 13, -71.6720008, 48.520525),
    Waypoint("November", 14, -71.6461702, 48.5090567),
    Waypoint("Oscar", 15, -71.6516848, 48.5107057),
    Waypoint("Papa", 16, -71.6298198, 48.5039667),
    Waypoint("Quebec", 17, -71.6345802, 48.5262308),
    Waypoint("Point 18", 18, -71.6804996, 48.511563),
    Waypoint("Romeo", 19, -71.6425625, 48.4984266),
    Waypoint("Sierra", 20, -71.6320911, 48.5258329),
    Waypoint("Tango", 21, -71.6758648, 48.4996779),
    Waypoint("Uniform", 22, -71.6290012, 48.4937058),
    Waypoint("Victor", 23, -71.6228085, 48.510353),
    Waypoint("Whiskey", 24, -71.6216069, 48.5093153),
    Waypoint("Xray", 25, -71.6034018, 48.4969248),
    Waypoint("Yankee", 26, -71.6312968, 48.5112557),
    Waypoint("Zulu", 27, -71.6664874, 48.4932846)
]


class WaypointList:

    def __init__(self):
        """Initialize List of Waypoint objects"""
        self.waypoints = {}
        for waypoint in ALL_WAYPOINTS:
            self.waypoints[waypoint.name] = waypoint

    def get_wp_by_name(self, name) -> Union[None, Waypoint]:
        """Returns waypoint associated with input name

        :param name: Waypoint name to search for (str)
        :return: Waypoint with given name, else None
        """
        if name in self.waypoints:
            return self.waypoints[name]
        return None

    def get_wp_by_num(self, number) -> Union[None, Waypoint]:
        """Returns waypoint associated with input number

        :param number: Waypoint number to search for (str)
        :return: Waypoint with given number, else None
        """
        for waypoint in self.waypoints:
            if waypoint.number == number:
                return waypoint
        return None


WAYPOINT_LST = WaypointList()
