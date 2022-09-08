import pytest

from basic_structures.classes import Classes
from basic_structures.room import Room


@pytest.fixture(scope='function')
def room() -> Room:
    return Room(id_=1,
                _initial_availability_minutes=5 * 8 * 60,
                people_capacity=32)


@pytest.fixture(scope='function')
def classes() -> Classes:
    return Classes(1, None, 20, None, None, None)


class ClassesMock(Classes):
    def __init__(self, val_or_none):
        super().__init__(1, None, None, None, None, None)
        self._amount = val_or_none

    @property
    def total_amount_of_students(self) -> int or None:
        return self._amount


class TestRoom:
    def test_priority_set(self, room):
        with pytest.raises(AttributeError):
            room.occupation_priority = 1

    def test_priority_get(self, room):
        room._occupation_priority = 1
        assert room.occupation_priority == 1

    def test_get_0_priority(self, room):
        room._occupation_priority = 0
        with pytest.raises(RuntimeError):
            _ = room.occupation_priority

    def test__calc_priority(self, room):
        room._initial_availability_minutes = 40.25
        room._current_occupation_minutes = 10.13
        room._predicted_occupation = 1.3
        room._calc_priority()
        assert room.occupation_priority == (40.25 - 10.13) / 1.3

    def test__calc_predicted_occupation(self, room):
        room._classes_occupation_probability = {1: 0.2, 2: 1, 3: 0.1}
        room._calc_predicted_occupation()
        assert room._predicted_occupation == 1.3

    def test__update(self, room):
        room._classes_occupation_probability = {1: 0.2, 2: 1, 3: 0.1}
        room._initial_availability_minutes = 40.25
        room._current_occupation_minutes = 10.13
        room._update()
        assert room._predicted_occupation == 1.3
        assert room.occupation_priority == (40.25 - 10.13) / 1.3

    def test_add_new_classes_to_room(self, room, classes):
        with pytest.raises(KeyError):
            _ = room._classes_occupation_probability[1]
        room.add_new_potential_classes_to_room(classes, 0.1)
        assert room._classes_occupation_probability[1] == 0.1
        assert room._const_classes_occupation_probability[1] == 0.1

    def test_add_new_classes_to_room__the_same_again(self, room, classes):
        room.add_new_potential_classes_to_room(classes, 0.2)
        with pytest.raises(RuntimeError):
            room.add_new_potential_classes_to_room(classes, 0.3)

    def test__set_probability_of_classes_correct(self, room, classes):
        room.add_new_potential_classes_to_room(classes, 0.1)
        room._set_probability_of_classes(classes.id_, 0.2)
        assert room._classes_occupation_probability[1] == 0.2

    def test__set_probability_of_classes_incorrect_id(self, room, classes):
        room.add_new_potential_classes_to_room(classes, 0.1)
        with pytest.raises(RuntimeError):
            room._set_probability_of_classes(2, 0.3)

    def test__reset_probability_of_classes(self, classes, room):
        room.add_new_potential_classes_to_room(classes, 0.1)
        room._set_probability_of_classes(classes.id_, 0.2)
        assert room._classes_occupation_probability[1] == 0.2
        room._reset_probability_of_classes(classes.id_)
        assert room._classes_occupation_probability[1] == 0.1

    def test___check_if_classes_is_available(self, room, classes):
        assert room._is_classes_available(1) is False
        room.add_new_potential_classes_to_room(classes, 0.2)
        room._is_classes_available(1)
        assert room._is_classes_available(2) is False

    def test_assign_occup(self, classes, room):
        room.add_new_potential_classes_to_room(classes, 0.2)
        start_occup = room._current_occupation_minutes
        room.assign(classes)
        assert start_occup + int(classes.duration) == room._current_occupation_minutes

    def test_assign__probability_and_priority_after_assign(self, classes, room):
        classes_2 = Classes(2, None, None, None, None, None)
        room.add_new_potential_classes_to_room(classes, 0.2)
        room.add_new_potential_classes_to_room(classes_2, 0.4)
        priority_before = room.occupation_priority
        room.assign(classes)
        assert room._classes_occupation_probability[1] == 0
        priority_after = room.occupation_priority
        assert priority_after != priority_before

    def test_assign__priority_exception_after_all_assignments(self, classes, room):
        classes_2 = Classes(2, None, 40, None, None, None)
        room.add_new_potential_classes_to_room(classes, 0.2)
        room.add_new_potential_classes_to_room(classes_2, 0.4)
        room.assign(classes)
        room.assign(classes_2)
        with pytest.raises(RuntimeError):
            _ = room.occupation_priority

    def test_unassign_occup(self, classes, room):
        room.add_new_potential_classes_to_room(classes, 0.2)
        room.assign(classes)
        start_occup = room._current_occupation_minutes
        room.unassign(classes)
        assert start_occup - int(classes.duration) == room._current_occupation_minutes

    def test_unassign__probability_and_priority_after_assign(self, classes, room):
        classes_2 = Classes(2, None, None, None, None, None)
        room.add_new_potential_classes_to_room(classes, 0.2)
        room.add_new_potential_classes_to_room(classes_2, 0.4)
        room.assign(classes)
        priority_before = room.occupation_priority
        room.unassign(classes)
        assert room._classes_occupation_probability[1] == 0.2
        priority_after = room.occupation_priority
        assert priority_after != priority_before


