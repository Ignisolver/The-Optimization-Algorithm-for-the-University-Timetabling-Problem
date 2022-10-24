from dataclasses import dataclass
from typing import Tuple, TYPE_CHECKING

from data import TIME_BETWEEN_ROOMS
from time_ import TimeDelta as TD, TimeDelta
from utils.types_ import RoomId, BuildingId

if TYPE_CHECKING:
    from basic_structures import Room


@dataclass
class Place:
    room: RoomId = None
    building: BuildingId = None


class Distances:
    def __init__(self):
        self._room_time = TIME_BETWEEN_ROOMS
        self._building_time_matrix = {}

    def __setitem__(self, b1_b2: Tuple["Room", "Room"], dist: TimeDelta):
        b1, b2 = b1_b2
        if b1 in self._building_time_matrix.keys():
            self._building_time_matrix[b1].update({b2: dist})
        else:
            self._building_time_matrix[b1] = {b2: dist}

    def __getitem__(self, b1_b2: Tuple["Room", "Room"]) -> TD:
        p1, p2 = b1_b2
        if p1 == p2:
            return TimeDelta(0, 0)

        try:
            dist = self._building_time_matrix[p1.build_id][p2.build_id]
        except KeyError:
            dist = self._building_time_matrix[p2.build_id][p1.build_id]

        return dist


DISTANCES = Distances()
