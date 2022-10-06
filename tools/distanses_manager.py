from dataclasses import dataclass
from typing import Tuple

from basic_structures import Room
from time_ import TimeDelta as TD, TimeDelta
from utils.types_ import RoomId, BuildingId


@dataclass
class Place:
    room: RoomId = None
    building: BuildingId = None


class Distances:
    def __init__(self):
        self._room_time_matrix = {}
        self._building_time_matrix = {}

    @staticmethod
    def _update_matrix(p1, p2, dist, matrix):
        if p1 in matrix.keys():
            matrix[p1].update({p2: dist})
        else:
            matrix[p1] = {p2: dist}

    def set_room_dist(self, p1: RoomId, p2: RoomId, dist: TD):
        self._update_matrix(p1, p2, dist, self._room_time_matrix)

    def set_building_dist(self, p1: BuildingId, p2: BuildingId, time: TD):
        self._update_matrix(p1, p2, time, self._building_time_matrix)

    def __getitem__(self, key: Tuple["Room", "Room"]) -> TD:
        p1, p2 = key
        if p1 == p2:
            return TimeDelta(0, 0)
        try:
            dist = self._room_time_matrix[p1.id_][p2.id_]
        except KeyError:
            try:
                dist = self._room_time_matrix[p2.id_][p1.id_]
            except KeyError:
                try:
                    dist = self._building_time_matrix[p1.build_id][p2.build_id]
                except KeyError:
                    dist = self._building_time_matrix[p2.build_id][p1.build_id]
        return dist


DISTANCES = Distances()
