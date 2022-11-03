from dataclasses import dataclass
from typing import Tuple, TYPE_CHECKING

from data import TIME_BETWEEN_ROOMS
from time_ import TimeDelta as TD, TimeDelta
from utils.singleton import SingletonMeta
from utils.types_ import RoomId, BuildingId

if TYPE_CHECKING:
    from basic_structures.room import Building
    from basic_structures import Room


@dataclass
class Place:
    room: RoomId = None
    building: BuildingId = None


class Distances(metaclass=SingletonMeta):
    def __init__(self):
        self._room_time = TIME_BETWEEN_ROOMS
        self._building_time_matrix = {}

    def __setitem__(self, b1_b2: Tuple["Building", "Building"],
                    dist: "TimeDelta"):
        b1, b2 = b1_b2
        b1 = b1.id_
        b2 = b2.id_
        if b1 == b2:
            return
        if b1 in self._building_time_matrix.keys():
            self._building_time_matrix[b1].update({b2: dist})
        else:
            self._building_time_matrix[b1] = {b2: dist}

    def __getitem__(self, b1_b2: Tuple["Room", "Room"]) -> "TD":
        p1, p2 = b1_b2
        if p1.id_ == p2.id_:
            return TimeDelta()
        if p1.build_id == p2.build_id:
            return self._room_time
        try:
            dist = self._building_time_matrix[p1.build_id][p2.build_id]
        except KeyError:
            dist = self._building_time_matrix[p2.build_id][p1.build_id]

        return dist
