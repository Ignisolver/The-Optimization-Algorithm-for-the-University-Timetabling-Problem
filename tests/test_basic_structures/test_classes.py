import pytest

from basic_structures import Classes, Room, Lecturer, Group
from time_ import TimeDelta, Time
from utils.types_ import ClassesType, MONDAY


class WithScheduleMock:
    def __init__(self, _id):
        self.assigned = None
        self.id = _id

    def assign(self, classes: Classes):
        self.assigned = classes


@pytest.fixture
def classes():
    cl = Classes(1, "aa", TimeDelta(1, 20), ClassesType.LECTURE,
                 [Room(1, 200, 30)],
                 WithScheduleMock(2), [WithScheduleMock(1)])
    return cl


def test__assign_to_room_groups_lecturer(classes):
    classes.start_time = Time(10,20)
    classes.room = WithScheduleMock(3)
    classes.day = MONDAY
    classes._assign_to_room_groups_lecturer()
    assert classes.lecturer.assigned == classes
    assert classes.room.assigned == classes
    assert classes.groups[0].assigned == classes


def test_assign(classes):
    classes.assign(Time(10,20), WithScheduleMock(3), MONDAY)
    assert classes.lecturer.assigned == classes
    assert classes.room.assigned == classes
    assert classes.day == MONDAY
    assert classes.room.id == 3
    assert classes.lecturer.id == 2
    assert classes.start_time == Time(10,20)
    assert classes.end_time == Time(11,40)
    assert classes.groups[0].assigned == classes


def test_start_time(classes):
    classes.start_time = Time(10,20)
    assert classes.start_time == Time(10,20)
    assert classes.end_time == Time(11,40)


def test_pretty_represent(classes):
    classes.start_time = Time(10,20)
    print()
    classes.pretty_represent()

