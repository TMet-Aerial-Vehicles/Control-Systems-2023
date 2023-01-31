from abc import ABC, abstractmethod
import re
from enum import Enum

from waypoint import WAYPOINT_LST
from route import Route
from utils import success_dict, error_dict

# QR Codes from ConOps
qr_example_1 = "Follow route Waypoint 3; Waypoint 14; Waypoint 6; Waypoint 12;\
 Waypoint 1"
qr_example_2 = "Avoid the area bounded by Waypoint 3; Waypoint 7; Waypoint 4;\
 Waypoint 2. Rejoin the route at Waypoint 13"
qr_example_3 = "Route number 1; 2 pers; Waypoint 12; Waypoint 3; 15 kg;\
 obstacle 2 m to NE; $112 Route number 2; 6 pers; Waypoint 3; Waypoint 7;\
 5 kg; nil; $50 Route number 3; 4 pers; Waypoint 7; Waypoint 8; 15 kg; \
 other comment; $150"

updated_qr_1 = "Follow route: Quebec; Lima; Alpha; Tango"
updated_qr_2 = "Avoid the area bounded by: Zulu; Bravo; Tango; Uniform.\
  Rejoin the route at Lima"
updated_qr_3 = "Route number 1: 2 pers; Lima; Quebec; 15 kg;\
 obstacle 2 m to NE; $112\
Route number 2: 6 pers; Delta; Charlie; 5 kg; nil; $50\
Route number 3: 4 pers; Alpha; Zulu; 15 kg; other comment; $150"


class QrTypes(Enum):
    Task_1_Initial_Qr = 1
    Task_1_Update_Qr = 2
    Task_2_Qr = 3


class QrHandler:
    """Holds instance of all QR objects"""

    def __init__(self):
        self.qrs = [Qr1(), Qr2(), Qr3()]

    def reset_qr(self, qr_type) -> None:
        """Reset QR to initial default

        :param qr_type: The QR to reset (int)
        :return: None
        """
        if qr_type == 1:
            self.qrs[0] = Qr1()
        elif qr_type == 2:
            self.qrs[1] = Qr2()
        elif qr_type == 2:
            self.qrs[2] = Qr3()

    def process_qr(self, qr_type: str, raw_qr_str: str):
        """Process QR, extracting and converting into routes

        :param qr_type: (str) Expected QR Type
        :param raw_qr_str: (str) Raw data extracted from QR
        :return: API Response Dict
        """
        try:
            qr_type_int = int(qr_type) - 1
            if 1 <= qr_type_int <= 3:
                if self.qrs[qr_type_int].is_valid(raw_qr_str):
                    return self.qrs[qr_type_int].process(raw_qr_str)
                return error_dict(f"Invalid QR {qr_type} Format")
            return error_dict("Invalid QR Type [1-3]")
        except ValueError:
            return error_dict("Unable to identify QR Type Format")

    def get_qr(self, qr_type: str, waypoints_as_dicts=True):
        """Returns the QR object data

        :param qr_type: (str) QR to return
        :param waypoints_as_dicts: (bool) Return waypoint or route objects as
                                   dictionaries or as objects
        :return: API Response dict containing QR data
        """
        try:
            qr_type_int = int(qr_type)
            if 1 <= qr_type_int <= 3:
                return {
                    "success": True,
                    "qr_type": qr_type,
                    "qr_data": self.qrs[qr_type_int - 1].convert_to_dict(
                                                            waypoints_as_dicts)
                }
            else:
                return error_dict("Invalid QR Type [1-3]")
        except ValueError:
            return error_dict("Unable to identify QR Type Format")


class Qr(ABC):
    """Abstract QR Class"""

    def __init__(self):
        self.raw_str = ""
        self.valid_qr_found = False

    @abstractmethod
    def is_valid(self, raw_str: str) -> bool:
        pass

    @abstractmethod
    def process(self, raw_str: str) -> dict:
        pass

    @abstractmethod
    def convert_to_dict(self, waypoints_as_dict=True) -> dict:
        pass


class Qr1(Qr):
    """
    QR 1 Example: "Follow route: Quebec; Lima; Alpha; Tango"
    """

    def __init__(self):
        Qr.__init__(self)
        self.qr_type = 1
        self.waypoints = []

    def is_valid(self, raw_str: str) -> bool:
        return True if "Follow route:" in raw_str else False

    def process(self, raw_str: str) -> dict:
        waypoints = []
        if self.is_valid(raw_str):
            self.raw_str = raw_str

            waypoint_names_str = raw_str.split("Follow route:")[1].strip()
            waypoint_names_lst = waypoint_names_str.split(";")

            # Get Waypoints from name
            for name in waypoint_names_lst:
                wp = WAYPOINT_LST.get_wp_by_name(name.strip())
                if wp:
                    waypoints.append(wp)

            # Verify
            if waypoints:
                self.valid_qr_found = True
                self.waypoints = waypoints
                return success_dict("QR 1 Found and Validated")
            else:
                return error_dict("0 Waypoints found in QR")
        else:
            return error_dict("Invalid QR Code String for QR Type 1")

    def convert_to_dict(self, wp_as_dict=True) -> dict:
        return {
            "qr_type": self.qr_type,
            "is_found": self.valid_qr_found,
            "raw_str": self.raw_str,
            "waypoints": ([wp.to_dict() for wp in self.waypoints]
                          if wp_as_dict else [wp for wp in self.waypoints])
        }


class Qr2(Qr):
    """
    Avoid the area bounded by: Zulu; Bravo; Tango; Uniform.  Rejoin the
        route at Lima
    """

    def __init__(self):
        Qr.__init__(self)
        self.qr_type = 2
        self.boundary_waypoints = []
        self.rejoin_waypoint = None

    def is_valid(self, raw_str: str) -> bool:
        if "Avoid the area bounded by:" in raw_str and \
                "Rejoin the route at" in raw_str:
            return True
        return False

    def process(self, raw_str: str) -> dict:
        boundary_waypoints = []
        if self.is_valid(raw_str):
            self.raw_str = raw_str

            bounds_rejoin_str = raw_str.split("Avoid the area bounded by:")[1]
            bounds_rejoin_lst = bounds_rejoin_str.split("Rejoin the route at")

            # Boundaries
            boundaries_str = bounds_rejoin_lst[0].strip(". ")
            boundaries_lst = boundaries_str.split(";")
            for name in boundaries_lst:
                wp = WAYPOINT_LST.get_wp_by_name(name.strip())
                if wp:
                    boundary_waypoints.append(wp)

            # Rejoin Waypoint
            waypoint_str = bounds_rejoin_lst[1].strip()
            rejoin_wp = WAYPOINT_LST.get_wp_by_name(waypoint_str)

            # Verify boundaries and rejoin waypoint
            if boundary_waypoints and rejoin_wp:
                self.valid_qr_found = True
                self.boundary_waypoints = boundary_waypoints
                self.rejoin_waypoint = rejoin_wp
                return success_dict("QR 2 Found and Validated")
            else:
                return error_dict("Error parsing waypoints in QR")
        else:
            return error_dict("Invalid QR Code String for QR Type 2")

    def convert_to_dict(self, wp_as_dict=True) -> dict:
        return {
            "qr_type": self.qr_type,
            "is_found": self.valid_qr_found,
            "raw_str": self.raw_str,
            # "boundaries": [wp.to_dict() for wp in self.boundary_waypoints],
            "boundaries": ([wp.to_dict() for wp in self.boundary_waypoints]
                           if wp_as_dict
                           else [wp for wp in self.boundary_waypoints]),
            "rejoin_waypoint": ((self.rejoin_waypoint.to_dict()
                                 if wp_as_dict else self.rejoin_waypoint)
                                if self.rejoin_waypoint is not None else None)
        }


class Qr3(Qr):
    """
    Route number 1: 2 pers; Lima; Quebec; 15 kg; obstacle 2 m to NE; $112
Route number 2: 6 pers; Delta; Charlie; 5 kg; nil; $50
Route number 3: 4 pers; Alpha; Zulu; 15 kg; other comment; $150
    """

    def __init__(self):
        Qr.__init__(self)
        self.qr_type = 3
        self.routes = []

    def is_valid(self, raw_str: str) -> bool:
        return True if "Route number 1:" in raw_str else False

    def process(self, raw_str: str) -> dict:
        routes = []

        if self.is_valid(raw_str):
            self.raw_str = raw_str

            # Create Route for each route in raw_str
            for route_str in raw_str.split("\n"):
                if "Route number" in route_str:
                    routes.append(process_route_str(route_str))

            # Verify route counts
            if routes and len(routes) == raw_str.count("Route number"):
                self.valid_qr_found = True
                self.routes = routes

                return success_dict("QR 3 Found and Validated")
            else:
                return error_dict("Error parsing routes in QR")
        else:
            return error_dict("Invalid QR Code String for QR Type 3")

    def convert_to_dict(self, wp_as_dict=True) -> dict:
        return {
            "qr_type": self.qr_type,
            "is_found": self.valid_qr_found,
            "raw_str": self.raw_str,
            "routes": ([route.to_dict() for route in self.routes]
                       if wp_as_dict else [route for route in self.routes])
        }


def process_route_str(route_str) -> Route:
    """Parse route string to create Route object

    :param route_str: raw_str line containing route details (str)
    :return: Route object from the processed route_str (Route)
    """
    "Route number 1: 2 pers; Lima; Quebec; 15 kg; obstacle 2 m to NE; $112"
    num_details = route_str.split(":")
    number = int(re.findall(r'\d+', num_details[0])[0])
    details = num_details[1].split(";")
    num_passengers = int(re.findall(r'\d+', details[0].strip())[0])
    max_weight = int(re.findall(r'\d+', details[3].strip())[0])
    reward = int(re.findall(r'\d+', details[5].strip())[0])
    return Route(number=number, num_passengers=num_passengers,
                 start_waypoint_name=details[1].strip(),
                 end_waypoint_name=details[2].strip(),
                 max_vehicle_weight=max_weight, remarks=details[4].strip(),
                 reward=reward)
