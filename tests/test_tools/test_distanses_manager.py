from dataclasses import dataclass

import pytest

from tools.distanses_manager import Distances
from utils.types_ import RoomId, BuildingId


@pytest.fixture
def distances():
    return Distances()


@dataclass
class RoomM:
    id_: RoomId = None
    build_id: BuildingId = None
    

class TestDistances:
    def test__update_matrix__new(self, distances):
        a = {}
        distances._update_matrix(1, 2, 3, a)
        assert a[1] == {2: 3}

    def test__update_matrix__add(self, distances):
        a = {1: {2: 3}}
        distances._update_matrix(1, 4, 5, a)
        assert a[1] == {2: 3, 4: 5}

    def test_set_room_dist(self, distances):
        distances.set_room_dist(1,2,3)
        assert distances._room_time_matrix[1] == {2: 3}
        distances.set_room_dist(1,4,5)
        assert distances._room_time_matrix[1] == {2: 3, 4: 5}

    def test_set_building_distance(self, distances):
        distances.set_building_dist(1, 2, 3)
        assert distances._building_time_matrix[1] == {2: 3}
        distances.set_building_dist(1, 4, 5)
        assert distances._building_time_matrix[1] == {2: 3, 4: 5}

    def test___getitem__(self, distances):
        distances.set_room_dist(1, 4, 5)
        assert distances[RoomM(1,None), RoomM(4, None)] == 5
        assert distances[RoomM(4,None), RoomM(1, None)] == 5
        distances.set_room_dist(1, 2, 3)
        assert distances[RoomM(1,None), RoomM(2, None)] == 3
        assert distances[RoomM(2,None), RoomM(1, None)] == 3
        distances.set_building_dist(7, 4, 9)
        assert distances[RoomM(None, 7), RoomM(None, 4)] == 9
        assert distances[RoomM(None, 4), RoomM(None, 7)] == 9
        distances.set_building_dist(1, 7, 11)
        assert distances[RoomM(None, 1), RoomM(None, 7)] == 11
        assert distances[RoomM(None, 7), RoomM(None, 1)] == 11
        distances.set_room_dist(1, 7, 11)
        distances.set_building_dist(1, 7, 17)
        assert distances[RoomM(1, 1), RoomM(7, 7)] == 11





