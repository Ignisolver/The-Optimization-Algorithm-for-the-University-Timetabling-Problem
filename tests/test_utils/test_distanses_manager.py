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

    def __hash__(self):
        return hash(self.id_)


class TestDistances:
    def test__update_matrix__new(self, distances):
        distances[RoomM(1, None), RoomM(2, None)] = 3
        assert distances._building_time_matrix[1] == {2: 3}

    def test__update_matrix__add(self, distances):
        distances._building_time_matrix = {1: {2: 3}}
        distances[RoomM(1, None), RoomM(4, None)] = 5
        assert distances._building_time_matrix[1] == {2: 3, 4: 5}

    def test___getitem__(self, distances):
        distances[RoomM(1, None), RoomM(4, None)] = 5
        assert distances[RoomM(None, 1), RoomM(None, 4)] == 5
        assert distances[RoomM(None, 4), RoomM(None, 1)] == 5
        distances[RoomM(1, None), RoomM(2, None)] = 3
        assert distances[RoomM(None, 1), RoomM(None, 2)] == 3
        assert distances[RoomM(None, 2), RoomM(None, 1)] == 3
        distances[RoomM(7, None), RoomM(4, None)] = 9
        assert distances[RoomM(None, 7), RoomM(None, 4)] == 9
        assert distances[RoomM(None, 4), RoomM(None, 7)] == 9
        distances[RoomM(1, None), RoomM(7, None)] = 11
        assert distances[RoomM(None, 1), RoomM(None, 7)] == 11
        assert distances[RoomM(None, 7), RoomM(None, 1)] == 11
        distances[RoomM(1, None), RoomM(7, None)]
        assert distances[RoomM(1, 1), RoomM(7, 7)] == 11

    def test__getitem__same(self, distances):
        distances[RoomM(1, None), RoomM(1, None)] = 5
        print(distances[RoomM(None, 1), RoomM(None, 1)])
