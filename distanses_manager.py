from dataclasses import dataclass
from typing import List

from time_ import TimeDelta
from types_ import RoomId, BuildingId


@dataclass
class Place:
    room: RoomId = None
    building: BuildingId = None


class DistancesManager:
    def __init__(self):
        self.distance_matrix = {}

    def add_distance(self, place_1, place_2, distance_p1_p2, distance_p2_p1=None):
        if distance_p2_p1 is None:
            distance_p2_p1 = distance_p1_p2

        self.distance_matrix[pla]

    def get_distance_between_buildings(self):
        pass

    def get_distances_between_rooms(self, room_1: RoomId, rooms_2: list) -> List[TimeDelta]:
        pass