import pytest

from classes import Classes, Assignation
from group import Group
from lecturer import Lecturer
from room import Room
from time_ import Time, TimeDelta

lecturer_1 = Lecturer(1)
lecturer_2 = Lecturer(2)
lecturer_3 = Lecturer(3)
group_1 = Group(1, 30)
group_2 = Group(2, 30)
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
    def test__assert_attribute_is_not_already_assigned(self, classes):
        classes._assert_attribute_is_not_already_assigned(False, "TestValue")
        with pytest.raises(RuntimeError):
            classes._assert_attribute_is_not_already_assigned(True, "TestValue")

    def test__assert_correct_argument_type__ok(self, classes):
        classes._assert_correct_assign_argument_type([1, 2, 3], int, "TestInt")
        classes._assert_correct_assign_argument_type([1.4, 2.5, 3.6], float, "TestFloat")

    def test__assert_correct_argument_type__incorrect(self, classes):
        with pytest.raises(ValueError):
            classes._assert_correct_assign_argument_type([1, 2, 3], float, "TestIntFloat")
        with pytest.raises(ValueError):
            classes._assert_correct_assign_argument_type([1.0, 2.0, 3.2], int, "TestFloatInt")

    def test__assert_assigned_object_in_available_list__ok(self, classes):
        classes._assert_assigned_object_in_available_list([1, 2, 3], [1, 2, 3, 4])

    def test__assert_assigned_object_in_available_list__incorrect(self, classes):
        with pytest.raises(ValueError):
            classes._assert_assigned_object_in_available_list([1, 2, 4], [1, 2])

    def test_assert_rooms_and_groups_input_correctness__incorrect_none_none(self, classes):
        with pytest.raises(RuntimeError):
            classes._assert_rooms_and_groups_input_correctness(None, None)

    def test_assert_rooms_and_groups_input_correctness__ok_pass_one_new(self, classes):
        classes._assert_rooms_and_groups_input_correctness(new_groups=(group_2,))
        classes._assert_rooms_and_groups_input_correctness(new_rooms=(room_2,))

    def test_assert_rooms_and_groups_input_correctness__check_ok_both_new(self, classes):
        gr_1 = Group(1,20)
        gr_2 = Group(2,31)
        r_1 = Room(1,2000,30)
        r_2 = Room(2,2000,30)
        classes._assert_rooms_and_groups_input_correctness(new_rooms=(r_2,r_1), new_groups=(gr_1, gr_2))

    def test_assert_rooms_and_groups_input_correctness__check_wrong_both_new(self, classes):
        gr_1 = Group(1, 20)
        gr_2 = Group(2, 31)
        r_1 = Room(1, 2000, 20)
        r_2 = Room(2, 2000, 10)
        with pytest.raises(RuntimeError):
            classes._assert_rooms_and_groups_input_correctness(new_rooms=(r_2, r_1), new_groups=(gr_1, gr_2))

    def test_assert_rooms_and_groups_input_correctness__check_ok_rooms_new_groups_was(self, classes):
        gr_1 = Group(1, 20)
        gr_2 = Group(2, 31)
        r_1 = Room(1, 2000, 30)
        r_2 = Room(2, 2000, 30)
        classes.groups = (gr_1, gr_2)
        classes._assert_rooms_and_groups_input_correctness(new_rooms=(r_2, r_1))

    def test_assert_rooms_and_groups_input_correctness__check_ok_groups_new_rooms_was(self, classes):
        gr_1 = Group(1, 20)
        gr_2 = Group(2, 31)
        r_1 = Room(1, 2000, 30)
        r_2 = Room(2, 2000, 30)
        classes._assigned_rooms = (r_1, r_2)
        classes._assert_rooms_and_groups_input_correctness(new_groups=(gr_1, gr_2))

    def test_assert_rooms_and_groups_input_correctness__check_incorrect_rooms_new_groups_was(self, classes):
        gr_1 = Group(1, 40)
        gr_2 = Group(2, 31)
        r_1 = Room(1, 2000, 30)
        r_2 = Room(2, 2000, 30)
        classes._groups = (gr_1, gr_2)
        with pytest.raises(RuntimeError):
            classes._assert_rooms_and_groups_input_correctness(new_rooms=(r_2, r_1))

    def test_assert_rooms_and_groups_input_correctness__check_incorrect_groups_new_rooms_was(self, classes):
        gr_1 = Group(1, 40)
        gr_2 = Group(2, 31)
        r_1 = Room(1, 2000, 30)
        r_2 = Room(2, 2000, 30)
        classes._assigned_rooms = (r_1, r_2)
        with pytest.raises(RuntimeError):
            classes._assert_rooms_and_groups_input_correctness(new_groups=(gr_1, gr_2))

    def test_assert_rooms_are_able_to_contain_groups__ok(self, classes):
        gr_1 = Group(1, 20)
        gr_2 = Group(2, 31)
        r_1 = Room(1, 2000, 30)
        r_2 = Room(2, 2000, 30)
        classes._assert_rooms_are_able_to_contain_groups(groups=(gr_1, gr_2), rooms=(r_1, r_2))

    def test_assert_rooms_are_able_to_contain_groups__ok_accurate(self, classes):
        gr_1 = Group(1, 40)
        gr_2 = Group(2, 31)
        r_1 = Room(1, 2000, 42)
        r_2 = Room(2, 2000, 29)
        classes._assert_rooms_are_able_to_contain_groups(groups=(gr_1, gr_2), rooms=(r_1, r_2))

    def test_assert_rooms_are_able_to_contain_groups__incorrect(self, classes):
        gr_1 = Group(1, 40)
        gr_2 = Group(2, 31)
        r_1 = Room(1, 2000, 30)
        r_2 = Room(2, 2000, 30)
        with pytest.raises(RuntimeError):
            classes._assert_rooms_are_able_to_contain_groups(groups=(gr_1, gr_2), rooms=(r_1, r_2))

    def test__assert_attribute_is_already_assigned__ok(self, classes):
        classes._attribute_assigned.time = True
        classes._attribute_assigned.rooms = True
        classes._attribute_assigned.groups = True
        classes._attribute_assigned.lecturers = True
        for attribute in classes._attribute_assigned:
            classes._assert_attribute_is_already_assigned(attribute, "Test")

    def test__assert_attribute_is_already_assigned__wrong(self, classes):
        classes._attribute_assigned.time = False
        classes._attribute_assigned.rooms = False
        classes._attribute_assigned.groups = False
        classes._attribute_assigned.lecturers = False
        for attribute in classes._attribute_assigned:
            with pytest.raises(RuntimeError):
                classes._assert_attribute_is_already_assigned(attribute, "Test")

    def test_assigned_lecturers__ok(self, classes):
        assert classes.assigned_lecturers is None
        classes.assigned_lecturers = (lecturer_2, lecturer_1)
        assert lecturer_1 in classes.assigned_lecturers
        assert lecturer_2 in classes.assigned_lecturers
        assert classes._attribute_assigned.lecturers is True

    def test_unassign_lecturers__ok(self, classes):
        classes.assigned_lecturers = (lecturer_2,)
        assert classes._attribute_assigned.lecturers is True
        del classes.assigned_lecturers
        assert classes._attribute_assigned.lecturers is False
        assert classes.assigned_lecturers is None

    def test_unassign_lecturers__already_unassigned(self, classes):
        classes.assigned_lecturers = (lecturer_2,)
        del classes.assigned_lecturers
        with pytest.raises(RuntimeError):
            del classes.assigned_lecturers

    def test_assign_lecturers__not_lecturer(self, classes):
        with pytest.raises(ValueError):
            classes.assigned_lecturers = (room_1,)

    def test_assign_lecturers__again(self, classes):
        classes.assigned_lecturers = (lecturer_2, lecturer_1)
        with pytest.raises(RuntimeError):
            classes.assigned_lecturers = (lecturer_2, lecturer_1)

    def test_assign_lecturers__unavailable(self, classes):
        with pytest.raises(ValueError):
            classes.assigned_lecturers = (lecturer_3,)

    def test_assign_groups__ok(self, classes):
        assert classes.groups is None
        classes.groups = (group_2, group_1)
        assert group_1 in classes.groups
        assert group_2 in classes.groups
        assert classes._attribute_assigned.groups is True

    def test_unassign_groups__ok(self, classes):
        classes.groups = (group_2,)
        assert classes._attribute_assigned.groups is True
        del classes.groups
        assert classes._attribute_assigned.groups is False
        assert classes.groups is None

    def test_unassign_groups__already_unassigned(self, classes):
        classes.groups = (group_2,)
        del classes.groups
        with pytest.raises(RuntimeError):
            del classes.groups

    def test_assign_groups__not_group(self, classes):
        with pytest.raises(ValueError):
            classes.groups = (room_1,)

    def test_assign_groups__again(self, classes):
        classes.groups = (group_2, group_1)
        with pytest.raises(RuntimeError):
            classes.groups = (group_2, group_1)

    def test_assign_rooms__ok(self, classes):
        assert classes.assigned_rooms is None
        classes.assigned_rooms = (room_2, room_1)
        assert room_1 in classes.assigned_rooms
        assert room_2 in classes.assigned_rooms
        assert classes._attribute_assigned.rooms is True

    def test_unassign_rooms__ok(self, classes):
        classes.assigned_rooms = (room_2,)
        assert classes._attribute_assigned.rooms is True
        del classes.assigned_rooms
        assert classes._attribute_assigned.rooms is False
        assert classes.assigned_rooms is None

    def test_unassign_rooms__already_unassigned(self, classes):
        classes.assigned_rooms = (room_2,)
        del classes.assigned_rooms
        with pytest.raises(RuntimeError):
            del classes.assigned_rooms

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
        assert classes._attribute_assigned.time is True

    def test_unassign_time__ok(self, classes):
        classes.start_time = time_1
        assert classes._attribute_assigned.time is True
        del classes.start_time
        assert classes._attribute_assigned.time is False
        assert classes.start_time is None
        assert classes.end_time is None

    def test_unassign_time__already_unassigned(self, classes):
        classes.start_time = time_1
        del classes.start_time
        with pytest.raises(RuntimeError):
            del classes.start_time

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

    def test_assert_correct_assignment__ok(self, classes):
        classes.assigned_rooms = (room_1,)
        classes.assigned_lecturers = (lecturer_2,)
        classes.groups = (group_2,)
        classes.start_time = Time(12, 20)
        classes._assert_correct_assignment()

    def test_assign(self, classes):
        assert any(classes._attribute_assigned) is False
        classes.assign(Time(10, 20), (room_1,), (lecturer_1,), (group_1,))
        assert all(classes._attribute_assigned) is True
        assert classes.groups is not None
        assert classes.assigned_rooms is not None
        assert classes.assigned_lecturers is not None
        assert classes.start_time is not None
        assert classes.end_time is not None

    def test_unassign(self, classes):
        assert any(classes._attribute_assigned) is False
        classes.assign(Time(10, 20), (room_1,), (lecturer_1,), (group_1,))
        assert all(classes._attribute_assigned) is True
        classes.unassign()
        assert any(classes._attribute_assigned) is False
        assert classes.groups is None
        assert classes.assigned_rooms is None
        assert classes.assigned_lecturers is None
        assert classes.start_time is None
        assert classes.end_time is None

    def test_amount_of_students__none(self, classes):
        assert classes.total_amount_of_students is None

    def test_amount_of_students__groups(self, classes):
        classes.groups = (Group(1,50), Group(2,80), Group(2,21))
        assert classes.total_amount_of_students == 151


@pytest.fixture(scope="function")
def assignation():
    return Assignation()


class TestAssignation:
    def test_is_all__ok_true(self, assignation):
        assignation.groups = True
        assignation.lecturers = True
        assignation.time = True
        assignation.rooms = True
        assert all(assignation) is True

    def test_is_all__ok_false_groups(self, assignation):
        assignation.groups = False
        assignation.lecturers = True
        assignation.time = True
        assignation.rooms = True
        assert all(assignation) is False

    def test_is_all__ok_false_rooms(self, assignation):
        assignation.groups = True
        assignation.lecturers = True
        assignation.time = True
        assignation.rooms = False
        assert all(assignation) is False

    def test_is_all__ok_false_lecturers(self, assignation):
        assignation.groups = True
        assignation.lecturers = False
        assignation.time = True
        assignation.rooms = True
        assert all(assignation) is False

    def test_is_all__ok_false_time(self, assignation):
        assignation.groups = False
        assignation.lecturers = True
        assignation.time = False
        assignation.rooms = True
        assert all(assignation) is False

    def test_is_any__ok(self, assignation):
        assignation.groups = False
        assignation.lecturers = True
        assignation.time = True
        assignation.rooms = True
        assert any(assignation) is True

        assignation.groups = True
        assignation.lecturers = True
        assignation.time = False
        assignation.rooms = True
        assert any(assignation) is True

    def test_is_any_wrong(self, assignation):
        assignation.groups = False
        assignation.lecturers = False
        assignation.time = False
        assignation.rooms = False
        assert any(assignation) is False


