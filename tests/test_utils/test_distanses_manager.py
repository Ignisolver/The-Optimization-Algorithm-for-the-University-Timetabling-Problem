from dataclasses import dataclass

import pytest

from utils.distanses_manager import Distances
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
        distances[1, 2] = 3
        assert distances._building_time_matrix[1] == {2: 3}

    def test__update_matrix__add(self, distances):
        distances._building_time_matrix = {1: {2: 3}}
        distances[1, 4] = 5
        assert distances._building_time_matrix[1] == {2: 3, 4: 5}

    def test___getitem__(self, distances):
        distances[1, 4] = 5
        assert distances[RoomM(None, 1), RoomM(None, 4)] == 5
        assert distances[RoomM(None, 4), RoomM(None, 1)] == 5
        distances[1, 2] = 3
        assert distances[RoomM(None, 1), RoomM(None, 2)] == 3
        assert distances[RoomM(None, 2), RoomM(None, 1)] == 3
        distances[7, 4] = 9
        assert distances[RoomM(None, 7), RoomM(None, 4)] == 9
        assert distances[RoomM(None, 4), RoomM(None, 7)] == 9
        distances[1, 7] = 11
        assert distances[RoomM(None, 1), RoomM(None, 7)] == 11
        assert distances[RoomM(None, 7), RoomM(None, 1)] == 11
        distances[1, 7] = 11
        assert distances[RoomM(1, 1), RoomM(7, 7)] == 11





