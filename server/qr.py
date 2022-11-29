from typing import Dict
from enum import Enum
from abc import ABC, abstractmethod
import re

from waypoint import WaypointList


qr_example_1 = "Follow route Waypoint 3; Waypoint 14; Waypoint 6; Waypoint 12; Waypoint 1"
qr_example_2 = "Avoid the area bounded by Waypoint 3; Waypoint 7; Waypoint 4; Waypoint 2. Rejoin the route at Waypoint 13"
qr_example_3 = "Route number 1; 2 pers; Waypoint 12; Waypoint 3; 15 kg; obstacle 2 m to NE; $112 Route number 2; 6 pers; Waypoint 3; Waypoint 7; 5 kg; nil; $50 Route number 3; 4 pers; Waypoint 7; Waypoint 8; 15 kg; other comment; $150"

WAYPOINT_LST = WaypointList()


class QrTypes(Enum):
    Task1Route = 1
    Task1Boundary = 2
    Task2 = 3


def error_dict(message) -> Dict:
    return {
        "success": False,
        "reason": message
    }


class AllQr:

    def __init__(self):
        self.qrs = [Qr1(), Qr2(), Qr3()]

    def reset_qr(self, qr_type) -> None:
        if qr_type == 1:
            self.qrs[0] = Qr1()
        elif qr_type == 2:
            self.qrs[1] = Qr2()
        elif qr_type == 2:
            self.qrs[2] = Qr3()


class Qr(ABC):

    def __init__(self):
        self.raw_str = ""
        self.valid_qr_found = False

    @abstractmethod
    def is_valid(self, raw_str: str) -> bool:
        pass

    @abstractmethod
    def process(self, raw_str: str) -> Dict:
        pass

    @abstractmethod
    def convert_to_dict(self):
        pass


class Qr1(Qr):

    def __init__(self):
        Qr.__init__(self)
        self.waypoints = []

    def is_valid(self, raw_str: str) -> bool:
        return True if "Follow route" in raw_str else False

    def process(self, raw_str: str) -> Dict:
        waypoints = []
        if self.is_valid(raw_str):
            self.raw_str = raw_str
            waypoint_nums = re.findall(r'\d+', raw_str)
            for num in waypoint_nums:
                wp = WAYPOINT_LST.get_wp_by_num(int(num))
                if wp:
                    waypoints.append(wp)
            if waypoints:
                self.valid_qr_found = True
                self.waypoints = waypoints
                return {
                    "success": True,
                    "message": "QR 1 Found and Validated"
                }
            else:
                return error_dict("0 Waypoints found in QR")
        else:
            return error_dict("Invalid QR Code String for QR Type 1")

    def convert_to_dict(self):
        vals = {
            "is_found": self.valid_qr_found,
            "raw_str": self.raw_str,
            "routes": [route.to_dict() for route in self.waypoints]
        }
        print(vals)
        return vals


class Qr2(Qr):

    def __init__(self):
        Qr.__init__(self)

    def is_valid(self, raw_str: str) -> bool:
        pass

    def process(self, raw_str: str) -> Dict:
        pass

    def convert_to_dict(self) -> Dict:
        return {
            "is_found": self.valid_qr_found,
            "raw_str": self.raw_str
        }


class Qr3(Qr):

    def __init__(self):
        Qr.__init__(self)

    def is_valid(self, raw_str: str) -> bool:
        pass

    def process(self, raw_str: str) -> Dict:
        pass

    def convert_to_dict(self):
        pass
