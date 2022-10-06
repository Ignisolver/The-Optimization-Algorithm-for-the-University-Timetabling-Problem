from dataclasses import dataclass
from typing import List

import pytest

from basic_structures import Classes
from schedule.day_scheadule import DaySchedule
from time_ import TimeDelta, Time
from utils.types_ import ClassesTypes as CT, ClassesType, ClassesTypes

DISTANCES = {(1, 0): TimeDelta(1, 0),
             (0, 1): TimeDelta(1, 0),
             (2, 3): TimeDelta(0, 20),
             (3, 2): TimeDelta(0, 20),
             (0, 2): TimeDelta(1, 0),
             (2, 3): TimeDelta(0, 20),
             }


@pytest.fixture
def day_schedule():
    return DaySchedule(1, _distances=DISTANCES)


@dataclass
class RoomM:
    id_: int
    building: int
    def __hash__(self):
        return self.id_

@dataclass
class ClassesM:
    dur: TimeDelta
    classes_type: ClassesType
    _assigned_rooms: List[RoomM]
    _start_t: Time = None

    def __post_init__(self):
        self._end_t = self._start_t + self.dur
        self.start_time = self._start_t
        self.end_time = self._end_t
        self.assigned_rooms = self._assigned_rooms

@dataclass
class DistM:
    dist = {0: {1: TimeDelta(0,10), 2: TimeDelta(0,20)},
            1: {2: TimeDelta(0,30)}
            }
    def __getitem__(self, key):
        a, b = key
        try:
            return self.dist[a.id_][b.id_]
        except:
            return self.dist[b.id_][a.id_]


@pytest.fixture
def day_schedule_1():
    return DaySchedule(1, _distances=DistM())


@pytest.fixture
def classes_list() -> List[Classes]:
    classes = [Classes(1, "nam1", TimeDelta(1, 20), CT.LECTURE, None, None),
               Classes(2, "nam2", TimeDelta(2, 20), CT.LABORATORY, None, None),
               Classes(3, "nam3", TimeDelta(1, 00), CT.LECTURE, None, None),
               Classes(4, "nam4", TimeDelta(2, 00), CT.LABORATORY, None, None),
               Classes(5, "nam5", TimeDelta(3, 30), CT.LECTURE, None, None),
               ]
    return classes



class TestDayScheadule:
    def test___len__(self, day_schedule, classes_list):
        day_schedule._classes = classes_list
        assert len(day_schedule) == int(TimeDelta(10, 10))

    def test___iter__(self, day_schedule):
        l = [1, 2, 3, 4, 5]
        day_schedule._classes = l
        for i in day_schedule:
            assert i in l

    def test_get_classes(self, day_schedule, classes_list):
        day_schedule._classes = classes_list
        assert day_schedule.get_classes() == classes_list

    def test__calc_time_between_classes(self, day_schedule, classes_list):
        cl1 = classes_list[0]
        cl1.start_time = Time(10, 20)
        cl1._assigned_rooms = [1]
        cl2 = classes_list[1]
        cl2.start_time = Time(14, 20)
        cl2._assigned_rooms = [0]
        assert day_schedule._calc_time_btw_classes(classes_list[0],
                                                   classes_list[1]) == \
               TimeDelta(1, 40)

    def test_get_free_time(self, day_schedule, classes_list):
        new_cl_list = []
        rooms = [2, 3, 2, 3]
        start_times = [Time(8, 0), Time(10,0), Time(13, 0), Time(15, 0)]
        for nr, cl in enumerate(classes_list[0: 4]):
            cl.start_time = start_times[nr]
            cl._assigned_rooms = [rooms[nr]]
            new_cl_list.append(cl)
        day_schedule._classes = new_cl_list
        assert day_schedule.get_free_time(min_h=Time(7, 0),
                                          max_h=Time(22,0)) == TimeDelta(7, 20)

    def test_get_brake_time(self, day_schedule, classes_list):
        new_cl_list = []
        rooms = [2, 3, 2, 3]
        start_times = [Time(8, 0), Time(10, 0), Time(13, 0), Time(15, 0)]
        for nr, cl in enumerate(classes_list[0: 4]):
            cl.start_time = start_times[nr]
            cl._assigned_rooms = [rooms[nr]]
            new_cl_list.append(cl)
        day_schedule._classes = new_cl_list
        assert day_schedule.get_brake_time() == TimeDelta(1, 20)

    def test_get_last_classes(self, day_schedule, classes_list):
        day_schedule._classes = classes_list
        assert day_schedule.get_last_classes() == classes_list[-1]

    def test_get_first_classes(self, day_schedule, classes_list):
        day_schedule._classes = classes_list
        assert day_schedule.get_first_classes() == classes_list[0]

    def test_get_amount_of_labs(self, day_schedule, classes_list):
        day_schedule._classes = classes_list
        assert day_schedule.get_amount_of_labs() == 2

    def test_get_amount_of_lectures(self, day_schedule, classes_list):
        day_schedule._classes = classes_list
        assert day_schedule.get_amount_of_lectures() == 3

    def test_get_amount_of_classes(self, day_schedule, classes_list):
        day_schedule._classes = classes_list
        assert day_schedule.get_amount_of_classes() == 5

    def test__assert_not_intersect__ok(self, day_schedule_1):
        cl1 = ClassesM(TimeDelta(1,0), None, [RoomM(0,44)], Time(10,0))
        cl2 = ClassesM(TimeDelta(1,0), None, [RoomM(1,55)], Time(13,0))
        # 9:40 - 11:20,  12:30 - 14:30
        day_schedule_1._classes = [cl1, cl2]

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(8, 0))
        day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(9, 0))
        day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(11, 0))
        day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(11, 30))
        day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(12, 00))
        day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(14, 0))
        day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(15, 50))
        day_schedule_1._assert_not_intersect(cl3)

    def test__assert_not_intersect__incorrect(self, day_schedule_1):
        cl1 = ClassesM(TimeDelta(1,0), None, [RoomM(0,44)], Time(10,0))
        cl2 = ClassesM(TimeDelta(1,0), None, [RoomM(1,55)], Time(13,0))
        # 9:40 - 11:20,  12:30 - 14:30
        day_schedule_1._classes = [cl1, cl2]

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(9, 10))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(0, 30), None, [RoomM(2, 66)], Time(10, 00))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(10, 00))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(0, 50), None, [RoomM(2, 66)], Time(10, 10))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(1,0), None, [RoomM(2, 66)], Time(10, 10))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_not_intersect(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(13, 50))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_not_intersect(cl3)

    def test__assert_distance_is_not_to_long__ok(self, day_schedule_1):
        cl1 = ClassesM(TimeDelta(1, 0), None, [RoomM(0, 44)], Time(10, 0))
        cl2 = ClassesM(TimeDelta(1, 0), None, [RoomM(1, 55)], Time(13, 0))
        # 9:40 - 11:20,  12:30 - 14:30
        day_schedule_1._classes = [cl1, cl2]

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(8, 0))
        day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(0, 40), None, [RoomM(2, 66)], Time(9, 0))
        day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(11, 20))
        day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(0, 50), None, [RoomM(2, 66)], Time(11, 30))
        day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(11, 30))
        day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(14, 30))
        day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(15, 0))
        day_schedule_1._assert_distance_is_not_to_long(cl3)

    def test__assert_distance_is_not_to_long__incorrect(self, day_schedule_1):
        cl1 = ClassesM(TimeDelta(1, 0), None, [RoomM(0, 44)], Time(10, 0))
        cl2 = ClassesM(TimeDelta(1, 0), None, [RoomM(1, 55)], Time(13, 0))
        # 9:40 - 11:20,  12:30 - 14:30
        day_schedule_1._classes = [cl1, cl2]

        cl3 = ClassesM(TimeDelta(0, 50), None, [RoomM(2, 66)], Time(9, 0))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(0, 5), None, [RoomM(2, 66)], Time(9, 50))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(0,40), None, [RoomM(2, 66)], Time(11,0))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(0, 4), None, [RoomM(2, 66)], Time(11, 10))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(0, 40), None, [RoomM(2, 66)], Time(11, 10))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_distance_is_not_to_long(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(14, 20))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_distance_is_not_to_long(cl3)

    def test__assert_assignment_available__ok(self, day_schedule_1,
                                              classes_list):

        cl1 = ClassesM(TimeDelta(1, 0), None, [RoomM(0, 44)], Time(10, 0))
        cl2 = ClassesM(TimeDelta(1, 0), None, [RoomM(1, 55)], Time(13, 0))
        # 9:40 - 11:20,  12:30 - 14:30
        day_schedule_1._classes = [cl1, cl2]

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(8, 0))
        day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(11, 30))
        day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(15, 50))
        day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(8, 0))
        day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 40), None, [RoomM(2, 66)], Time(9, 0))
        day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(11, 20))
        day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 50), None, [RoomM(2, 66)], Time(11, 30))
        day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(11, 30))
        day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(14, 30))
        day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(15, 0))
        day_schedule_1._assert_assignment_available(cl3)

    def test__assert_assignment_available__incorrect(self,
                                                     day_schedule_1,
                                                     classes_list):
        cl1 = ClassesM(TimeDelta(1, 0), None, [RoomM(0, 44)], Time(10, 0))
        cl2 = ClassesM(TimeDelta(1, 0), None, [RoomM(1, 55)], Time(13, 0))
        # 9:40 - 11:20,  12:30 - 14:30
        day_schedule_1._classes = [cl1, cl2]

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(9, 0))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 30), None, [RoomM(2, 66)], Time(9, 50))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 30), None, [RoomM(2, 66)], Time(10, 10))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 5), None, [RoomM(2, 66)], Time(11, 10))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 50), None, [RoomM(2, 66)], Time(10, 50))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(10, 00))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(11, 00))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(11, 5))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(13, 50))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 50), None, [RoomM(2, 66)], Time(9, 0))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 5), None, [RoomM(2, 66)], Time(9, 50))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 40), None, [RoomM(2, 66)], Time(11, 0))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 4), None, [RoomM(2, 66)], Time(11, 10))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(0, 40), None, [RoomM(2, 66)], Time(11, 10))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)

        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(14, 20))
        with pytest.raises(AssertionError):
            day_schedule_1._assert_assignment_available(cl3)
        
        

    def test__sort_classes_fcn(self, day_schedule_1, classes_list):
        cl1 = classes_list[0]
        cl1.start_time = Time(10, 0)
        assert day_schedule_1._sort_classes_fcn(cl1) == Time(10, 0)

    def test__sort_classes(self, day_schedule_1, classes_list):
        new_cl_list = []
        start_times = [Time(13, 0), Time(15, 0), Time(8, 0), Time(10, 0)]
        for nr, cl in enumerate(classes_list[0: 4]):
            cl.start_time = start_times[nr]
            new_cl_list.append(cl)
        day_schedule_1._classes = new_cl_list
        day_schedule_1._sort_classes()
        cl = classes_list
        corr_ord_cl_list = [cl[2], cl[3], cl[0], cl[1]]
        assert day_schedule_1._classes == corr_ord_cl_list

    def test_assign_classes_ok(self, day_schedule_1):
        cl1 = ClassesM(TimeDelta(1, 0), None, [RoomM(0, 44)], Time(10, 0))
        cl2 = ClassesM(TimeDelta(1, 0), None, [RoomM(1, 55)], Time(13, 0))
        # 9:40 - 11:20,  12:30 - 14:30
        day_schedule_1._classes = [cl1, cl2]
        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(8, 0))
        day_schedule_1.assign_classes(cl3)
        assert day_schedule_1._classes == [cl3, cl1, cl2]

    def test_assign_classes__incorrect(self, day_schedule_1):
        cl1 = ClassesM(TimeDelta(1, 0), None, [RoomM(0, 44)], Time(10, 0))
        cl2 = ClassesM(TimeDelta(1, 0), None, [RoomM(1, 55)], Time(13, 0))
        # 9:40 - 11:20,  12:30 - 14:30
        day_schedule_1._classes = [cl1, cl2]
        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(10, 0))
        with pytest.raises(AssertionError):
            day_schedule_1.assign_classes(cl3)

    def test_assign_temporary(self, day_schedule_1):
        cl1 = ClassesM(TimeDelta(1, 0), None, [RoomM(0, 44)], Time(10, 0))
        cl2 = ClassesM(TimeDelta(1, 0), None, [RoomM(1, 55)], Time(13, 0))
        # 9:40 - 11:20,  12:30 - 14:30
        day_schedule_1._classes = [cl1, cl2]
        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(8, 0))
        day_schedule_1.temp_assign(cl3)
        assert day_schedule_1._classes == [cl3, cl1, cl2]
        assert day_schedule_1._temp_cl_nr == 0

    def test_revert_temporary_assign(self, day_schedule_1):
        cl1 = ClassesM(TimeDelta(1, 0), None, [RoomM(0, 44)], Time(10, 0))
        cl2 = ClassesM(TimeDelta(1, 0), None, [RoomM(1, 55)], Time(13, 0))
        # 9:40 - 11:20,  12:30 - 14:30
        day_schedule_1._classes = [cl1, cl2]
        cl3 = ClassesM(TimeDelta(1, 0), None, [RoomM(2, 66)], Time(8, 0))
        day_schedule_1.temp_assign(cl3)
        assert day_schedule_1._classes == [cl3, cl1, cl2]
        assert day_schedule_1._temp_cl_nr == 0
        day_schedule_1.revert_temp_assign()
        assert day_schedule_1._temp_cl_nr == None
        assert day_schedule_1._classes == [cl1, cl2]

    def test_pretty_represent(self, day_schedule, classes_list):
        new_cl_list = []
        rooms = [2, 3, 2, 3]
        start_times = [Time(8, 0), Time(10, 0), Time(13, 0), Time(15, 0)]
        types = [ClassesType("W-E-3"), ClassesType("L-N-3"),
                 ClassesType("W-E-3"), ClassesType("L-N-3")]
        for nr, cl in enumerate(classes_list[0: 4]):
            cl.start_time = start_times[nr]
            cl._assigned_rooms = [rooms[nr]]
            cl.classes_type = types[nr]
            new_cl_list.append(cl)
        day_schedule._classes = new_cl_list
        print()
        day_schedule.pretty_represent()
