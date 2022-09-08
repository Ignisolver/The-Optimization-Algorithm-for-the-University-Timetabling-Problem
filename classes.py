from dataclasses import dataclass, field
from typing import Tuple, Iterable, Type

from group import Group
from lecturer import Lecturer
from room import Room
from time_ import Time, TimeDelta
from types_ import ClassesType, ClassesId
from utils import check_type_all, check_if_time_is_available


@dataclass
class Assignation:
    lecturers: bool = False
    groups: bool = False
    rooms: bool = False
    time: bool = False

    def __iter__(self):
        return iter((self.groups, self.rooms, self.time, self.lecturers))

# todo multi lecturer, group, room, classes
# todo przypisywanie do każdego elementu w środku podczas przypisywania zajęć
# todo uzupełnić klasę time


@dataclass
class Classes:
    id_: ClassesId
    name: str
    duration: TimeDelta
    classes_type: ClassesType
    available_rooms: Tuple[Room, ...]
    available_lecturers: Tuple[Lecturer, ...]
    _attribute_assigned: Assignation = field(default_factory=Assignation)
    _groups: Tuple[Group, ...] or None = None
    _assigned_lecturers: Tuple[Lecturer, ...] or None = None
    _assigned_rooms: Tuple[Room, ...] or None = None
    _start_time: Time or None = None
    _end_time: Time or None = None

    def assign(self,
               time: Time = None,
               rooms: Tuple[Room, ...] = None,
               lecturers: Tuple[Lecturer, ...] = None,
               groups: Tuple[Group, ...] = None):
        if lecturers is not None:
            self.assigned_lecturers = lecturers
        if groups is not None:
            self.groups = groups
        if rooms is not None:
            self.assigned_rooms = rooms
        if time is not None:
            self.start_time = time
        self._assert_correct_assignment()

    def unassign(self):
        del self.assigned_lecturers
        del self.assigned_rooms
        del self.start_time
        del self.groups

    @property
    def total_amount_of_students(self) -> int or None:
        if self.groups is None:
            return None
        else:
            total_amount = 0
            for group in self.groups:
                total_amount += group.amount_of_students
            return total_amount

    @property
    def groups(self):
        return self._groups

    @property
    def assigned_lecturers(self):
        return self._assigned_lecturers

    @property
    def assigned_rooms(self):
        return self._assigned_rooms

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @groups.setter
    def groups(self, groups: Tuple[Group, ...]):
        self._assert_assignment_is_available(self._attribute_assigned.groups, "Groups", groups, Group)
        self._groups = groups
        self._attribute_assigned.groups = True

    @assigned_lecturers.setter
    def assigned_lecturers(self, lecturers: Tuple[Lecturer, ...]):
        self._assert_assignment_is_available(self._attribute_assigned.lecturers, "Lecturers", lecturers, Lecturer,
                                             self.available_lecturers)
        self._assigned_lecturers = lecturers
        self._attribute_assigned.lecturers = True

    @assigned_rooms.setter
    def assigned_rooms(self, rooms: Tuple[Room, ...]):
        self._assert_assignment_is_available(self._attribute_assigned.rooms, "Rooms", rooms, Room, self.available_rooms)
        self._assigned_rooms = rooms
        self._attribute_assigned.rooms = True

    @start_time.setter
    def start_time(self, start_time: Time):
        self._assert_attribute_is_not_already_assigned(self._attribute_assigned.time, "Start time")
        self._assert_correct_assign_argument_type([start_time], Time, " Start time")
        end_time = start_time + self.duration
        check_if_time_is_available((start_time, end_time))
        self._start_time = start_time
        self._end_time = end_time
        self._attribute_assigned.time = bool(start_time)

    @groups.deleter
    def groups(self):
        self._assert_attribute_is_already_assigned(self._attribute_assigned.groups, "Groups")
        self._groups = None
        self._attribute_assigned.groups = False

    @assigned_lecturers.deleter
    def assigned_lecturers(self):
        self._assert_attribute_is_already_assigned(self._attribute_assigned.lecturers, "Lecturers")
        self._assigned_lecturers = None
        self._attribute_assigned.lecturers = False

    @assigned_rooms.deleter
    def assigned_rooms(self):
        self._assert_attribute_is_already_assigned(self._attribute_assigned.rooms, "Rooms")
        self._assigned_rooms = None
        self._attribute_assigned.rooms = False

    @start_time.deleter
    def start_time(self):
        self._assert_attribute_is_already_assigned(self._attribute_assigned.time, "Time")
        self._start_time = None
        self._end_time = None
        self._attribute_assigned.time = False

    def _assert_correct_assignment(self):
        if not all(self._attribute_assigned):
            raise RuntimeError(f"An attempt to assign classes without assign: {self._attribute_assigned}")

    @staticmethod
    def _assert_attribute_is_not_already_assigned(is_attribute_assigned, name):
        if is_attribute_assigned:
            raise RuntimeError(f"{name} already assigned")

    @staticmethod
    def _assert_attribute_is_already_assigned(is_attribute_assigned, name):
        if not is_attribute_assigned:
            raise RuntimeError(f"{name} attribute is not assigned yet - an attempt to unassign!")

    @staticmethod
    def _assert_correct_assign_argument_type(argument: Iterable or None,
                                             type_: Type,
                                             name: str):
        if len(argument) == 0 or (not check_type_all(argument, type_)):
            raise ValueError(f"Argument invalid '{name}': {argument}")

    @staticmethod
    def _assert_assigned_object_in_available_list(assigned, available):
        if not all(map(lambda x: x in available, assigned)):
            raise ValueError(f"Trying to assign unavailable object: {assigned} not in {available}")

    def _assert_assignment_is_available(self, is_attribute_assigned, name, new_attribute, arg_type, available_list=None):
        self._assert_attribute_is_not_already_assigned(is_attribute_assigned, name)
        self._assert_correct_assign_argument_type(new_attribute, arg_type, name)
        if available_list is not None:
            self._assert_assigned_object_in_available_list(new_attribute, available_list)

    @staticmethod
    def _assert_rooms_are_able_to_contain_groups(groups: Iterable[Group], rooms: Iterable[Room]):
        amount_of_student_in_groups = sum(group.amount_of_students for group in groups)
        capacity_in_rooms = sum(room.people_capacity for room in rooms)
        if capacity_in_rooms < amount_of_student_in_groups:
            raise RuntimeError("There is no enough space for all groups in rooms")

    def _assert_rooms_and_groups_input_correctness(self, new_groups=None, new_rooms=None):
        # Invalid usage
        if (new_rooms is None) and (new_groups is None):
            raise RuntimeError("Invalid usage of function")
        # An attempt to assign sth when other is nor assigned yet
        if ((new_rooms is None) and (self.assigned_rooms is None) and (new_groups is not None) or
                (new_groups is None) and (self.groups is None) and (new_rooms is not None)):
            pass
        # Sth is assigned - check if it is possible
        if (self.assigned_rooms is not None) and (new_groups is not None):
            self._assert_rooms_are_able_to_contain_groups(new_groups, self.assigned_rooms)
        if (self.groups is not None) and (new_rooms is not None):
            self._assert_rooms_are_able_to_contain_groups(self.groups, new_rooms)
        if ((new_groups is not None) and (new_rooms is not None) and
                (self.groups is None) and (self.assigned_rooms is None)):
            self._assert_rooms_are_able_to_contain_groups(new_groups, new_rooms)












