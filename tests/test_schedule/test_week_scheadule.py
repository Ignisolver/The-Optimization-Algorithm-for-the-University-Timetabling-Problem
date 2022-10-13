import pytest

from basic_structures import Classes, Room, Lecturer
from basic_structures.classes import UnavailableClasses
from schedule.week_scheadule import WeekSchedule
from time_ import TimeDelta, Time
from utils.types_ import ClassesType, MONDAY, FRIDAY, WEDNESDAY, LecturerId


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


@pytest.fixture(scope="function")
def week_schedule():
    return WeekSchedule()

@pytest.fixture()
def u_c():
    return [UnavailableClasses(Time(10, 30), TimeDelta(1, 0), MONDAY),
            UnavailableClasses(Time(14, 30), TimeDelta(2, 0), MONDAY)]


@pytest.fixture(scope="function")
def unav_ws(u_c) -> WeekSchedule:
    ws = WeekSchedule(u_c)
    return ws


@pytest.fixture(scope="function")
def cl():
    cl = Classes(1, "aa", TimeDelta(1, 20), ClassesType.LECTURE,
            [1, 2, 3], Lecturer(1,"lect"), [1, 2, 4], day=MONDAY)
    cl.start_time = Time(10, 40)
    return cl


def test_unavailable_initialisation(unav_ws, u_c):
    assert unav_ws.days[MONDAY].get_last_classes() == u_c[1]
    assert unav_ws.days[MONDAY].get_first_classes() == u_c[0]


def test_unavailable_assign(unav_ws, cl):
    with pytest.raises(AssertionError):
        unav_ws.assign(cl)


def test_assign(week_schedule, cl):
    week_schedule.assign(cl)
    assert week_schedule.days[MONDAY].get_first_classes() == cl


def test_temp_assign_unassign(week_schedule, cl):
    week_schedule.temp_assign(cl)
    assert week_schedule.days[MONDAY].get_first_classes() == cl
    week_schedule.unassign_temp()
    assert week_schedule.days[MONDAY].get_first_classes() is None


def test_to_yaml(unav_ws, cl):
    cl.day = WEDNESDAY
    cl.lecturer = Lecturer(1, "Adam")
    cl.room = Room(1, 100, 100, "402")
    unav_ws.assign(cl)
    print()
    print(unav_ws.to_yaml())

