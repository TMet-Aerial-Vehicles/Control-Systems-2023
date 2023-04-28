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

    def __eq__(self, other):
        if self.number == other.number:
            return True
        return False

    def __str__(self):
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.name}"

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
    Waypoint("Alpha", 1, -71.646305, 48.510012),
    Waypoint("Bravo", 2, -71.631752, 48.506095),
    Waypoint("Charlie", 3, -71.635096, 48.496972),
    Waypoint("Delta", 4, -71.643231, 48.515011),
    Waypoint("Echo", 5, -71.6407195, 48.5029013),
    Waypoint("Foxtrot", 6, -71.634186, 48.508072),
    Waypoint("Golf", 7, -71.6459941, 48.5079538),
    Waypoint("Hotel", 8, -71.642601, 48.512992),
    Waypoint("India", 9, -71.643298, 48.511464),
    Waypoint("Juliette", 10, -71.6491457, 48.5133384),
    Waypoint("Kilo", 11, -71.633141, 48.499458),
    Waypoint("Lima", 12, -71.626592, 48.504977),
    Waypoint("Mike", 13, -71.65131, 48.51409),
    Waypoint("November", 14, -71.641643, 48.507877),
    Waypoint("Oscar", 15, -71.641327, 48.514158),
    Waypoint("Papa", 16, -71.629971, 48.503998),
    Waypoint("Quebec", 17, -71.641189, 48.5069),
    Waypoint("Point 18", 18, -71.635331, 48.505351),
    Waypoint("Romeo", 19, -71.6372898, 48.5125668),
    Waypoint("Sierra", 20, -71.646339, 48.504569),
    Waypoint("Tango", 21, -71.651899, 48.512783),
    Waypoint("Uniform", 22, -71.632982, 48.494317),
    Waypoint("Victor", 23, -71.625827, 48.50901),
    Waypoint("Whiskey", 24, -71.629868, 48.506956),
    Waypoint("Xray", 25, -71.639107, 48.508981),
    Waypoint("Yankee", 26, -71.625435, 48.507311),
    Waypoint("Zulu", 27, -71.6469554, 48.5149672)
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
