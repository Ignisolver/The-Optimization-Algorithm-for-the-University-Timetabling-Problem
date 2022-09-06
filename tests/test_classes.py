import pytest

from classes import Classes, Assignation
from group import Group
from lecturer import Lecturer
from room import Room
from time_ import Time, TimeDelta

lecturer_1 = Lecturer()
lecturer_2 = Lecturer()
lecturer_3 = Lecturer()
group_1 = Group()
group_2 = Group()
room_1 = Room(1, 2, 4)
room_2 = Room(2, 2, 4)
room_3 = Room(3, 2, 4)
time_1 = Time(12, 40)
time_2 = Time(10, 20)
time_3 = Time(14, 10)


@pytest.fixture(scope="function")
def classes() -> Classes:
    return Classes(0, "testowe", TimeDelta(0, 50),
                   None, (room_1, room_2), (lecturer_1, lecturer_2))


class TestClasses:
    def test_assigned_lecturers__ok(self, classes):
        assert classes.assigned_lecturers is None
        classes.assigned_lecturers = (lecturer_2, lecturer_1)
        assert lecturer_1 in classes.assigned_lecturers
        assert lecturer_2 in classes.assigned_lecturers

    def test_assign_lecturers__not_lecturer(self, classes):
        with pytest.raises(ValueError):
            classes.assigned_lecturers = (room_1,)

    def test_assign_lecturers__again(self, classes):
        classes.assigned_lecturers = (lecturer_2, lecturer_1)
        with pytest.raises(RuntimeError):
            classes.assigned_lecturers = (lecturer_2, lecturer_1)

    def test_assign_lecturers__unavailable(self, classes):
        with pytest.raises(ValueError):
            classes.assigned_lecturers= (lecturer_3,)

    def test__check_if_attribute_is_not_already_assigned(self, classes):
        classes._check_if_attribute_is_not_already_assigned(None, "TestValue")
        with pytest.raises(RuntimeError):
            classes._check_if_attribute_is_not_already_assigned(True, "TestValue")

    def test__check_argument_type__ok(self, classes):
        classes._check_assign_argument_type([1, 2, 3], int, "TestInt")
        classes._check_assign_argument_type([1.4, 2.5, 3.6], float, "TestFloat")

    def test__check_argument_type__incorrect(self, classes):
        with pytest.raises(ValueError):
            classes._check_assign_argument_type([1, 2, 3], float, "TestIntFloat")
        with pytest.raises(ValueError):
            classes._check_assign_argument_type([1.0, 2.0, 3.2], int, "TestFloatInt")
            
    def test__check_if_is_in_available__ok(self, classes):
        classes._check_if_assigned_object_is_in_available_list([1, 2, 3], [1, 2, 3, 4])

    def test__check_if_is_in_available__incorrect(self, classes):
        with pytest.raises(ValueError):
            classes._check_if_assigned_object_is_in_available_list([1, 2, 4], [1, 2])

    def test_assign_groups__ok(self, classes):
        assert classes.groups is None
        classes.groups= (group_2, group_1)
        assert group_1 in classes.groups
        assert group_2 in classes.groups

    def test_assign_groups__not_group(self, classes):
        with pytest.raises(ValueError):
            classes.groups= (room_1,)

    def test_assign_groups__again(self, classes):
        classes.groups = (group_2, group_1)
        with pytest.raises(RuntimeError):
            classes.groups = (group_2, group_1)
                  
    def test_assign_rooms__ok(self, classes):
        assert classes.assigned_rooms is None
        classes.assigned_rooms = (room_2, room_1)
        assert room_1 in classes.assigned_rooms
        assert room_2 in classes.assigned_rooms

    def test_assign_rooms__not_room(self, classes):
        with pytest.raises(ValueError):
            classes.assigned_rooms = (lecturer_2,)

    def test_assign_rooms__again(self, classes):
        classes.assigned_rooms = (room_2, room_1)
        with pytest.raises(RuntimeError):
            classes.assigned_rooms = (room_2, room_1)

    def test_assign_rooms__unavailable(self, classes):
        with pytest.raises(ValueError):
            classes.assigned_rooms = (room_3,)

    def test_assign_time__ok(self, classes):
        assert classes._start_time is None
        assert classes._end_time is None
        classes.start_time = Time(10, 20)
        assert Time(10, 20) == classes._start_time
        assert Time(10, 20) + classes.duration == classes._end_time

    def test_assign_time__not_lecturer(self, classes):
        with pytest.raises(ValueError):
            classes.start_time = room_1

    def test_assign_time__again(self, classes):
        classes.start_time = Time(10, 20)
        with pytest.raises(RuntimeError):
            classes.start_time = Time(10, 30)

    def test_assign_time__unavailable(self, classes):
        with pytest.raises(ValueError):
            classes.start_time = Time(23, 0)
        print(classes)

    def test_correct_assignment__ok(self, classes):
        classes.assigned_rooms = (room_1,)
        classes.assigned_lecturers = (lecturer_2,)
        classes.groups = (group_2, )
        classes.start_time = Time(12, 20)
        classes._check_correct_assignment()

    def test_assign(self, classes):
        assert classes._attribute_assigned.is_any_assigned() is False
        classes.assign(Time(10,20), (room_1,), (lecturer_1,), (group_1,))
        assert classes._attribute_assigned.is_all_assigned() is True
        assert classes.groups is not None
        assert classes.assigned_rooms is not None
        assert classes.assigned_lecturers is not None
        assert classes.start_time is not None
        assert classes.end_time is not None
    
    def test_unassign(self, classes):
        assert classes._attribute_assigned.is_any_assigned() is False
        classes.assign(Time(10, 20), (room_1,), (lecturer_1,), (group_1,))
        assert classes._attribute_assigned.is_all_assigned() is True
        classes.unassign()
        assert classes._attribute_assigned.is_any_assigned() is False
        assert classes.groups is None
        assert classes.assigned_rooms is None
        assert classes.assigned_lecturers is None
        assert classes.start_time is None
        assert classes.end_time is None
        




@pytest.fixture(scope="function")
def assignation():
    return Assignation()


class TestAssignation:
    def test_is_all__ok_true(self, assignation):
        assignation.groups = True
        assignation.lecturers = True
        assignation.time = True
        assignation.rooms = True
        assert assignation.is_all_assigned() is True

    def test_is_all__ok_false_groups(self, assignation):
        assignation.groups = False
        assignation.lecturers = True
        assignation.time = True
        assignation.rooms = True
        assert assignation.is_all_assigned() is False

    def test_is_all__ok_false_rooms(self, assignation):
        assignation.groups = True
        assignation.lecturers = True
        assignation.time = True
        assignation.rooms = False
        assert assignation.is_all_assigned() is False

    def test_is_all__ok_false_lecturers(self, assignation):
        assignation.groups = True
        assignation.lecturers = False
        assignation.time = True
        assignation.rooms = True
        assert assignation.is_all_assigned() is False

    def test_is_all__ok_false_time(self, assignation):
        assignation.groups = False
        assignation.lecturers = True
        assignation.time = False
        assignation.rooms = True
        assert assignation.is_all_assigned() is False

    def test_is_any__ok(self, assignation):
        assignation.groups = False
        assignation.lecturers = True
        assignation.time = True
        assignation.rooms = True
        assert assignation.is_any_assigned() is True

        assignation.groups = True
        assignation.lecturers = True
        assignation.time = False
        assignation.rooms = True
        assert assignation.is_any_assigned() is True

    def test_is_any_wrong(self, assignation):
        assignation.groups = False
        assignation.lecturers = False
        assignation.time = False
        assignation.rooms = False
        assert assignation.is_any_assigned() is False