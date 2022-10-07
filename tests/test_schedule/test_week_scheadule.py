import pytest

from basic_structures import Classes, Room
from schedule.week_scheadule import WeekSchedule
from time_ import TimeDelta
from utils.types_ import ClassesType


class WithScheduleMock:
    def __init__(self, _id):
        self.assigned = None
        self.id = _id

@pytest.fixture
def classes():
    cl = Classes(1, "aa", TimeDelta(1, 20), ClassesType.LECTURE,
                 [Room(1, 200, 30)],
                 WithScheduleMock(2), [WithScheduleMock(1)])
    return cl

@pytest.fixture
def week_schedule():
    return WeekSchedule()


def test_assign():
    assert False


def test_temp_assign():
    assert False


def test_unassign_temp():
    assert False
