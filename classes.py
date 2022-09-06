from dataclasses import dataclass, field, fields
from typing import List, Tuple, Iterable, Type

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

    def is_all_assigned(self):
        return all((self.lecturers, self.groups, self.rooms, self.time))

    def is_any_assigned(self):
        return any((self.lecturers, self.groups, self.rooms, self.time))


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

    @staticmethod
    def _check_if_attribute_is_not_already_assigned(is_attribute_assigned, name):
        if is_attribute_assigned:
            raise RuntimeError(f"{name} already assigned")

    @staticmethod
    def _check_assign_argument_type(argument: Iterable or None,
                             type_: Type,
                             name: str):
        if len(argument) == 0 or (not check_type_all(argument, type_)):
            raise ValueError(f"Argument invalid '{name}': {argument}")

    @staticmethod
    def _check_if_assigned_object_is_in_available_list(assigned, available):
        if not all(map(lambda x: x in available, assigned)):
            raise ValueError(f"Trying to assign unavailable object: {assigned} not in {available}")

    def _check_if_assignment_is_available(self, is_attribute_assigned, name, new_attribute, arg_type, available_list=None):
        self._check_if_attribute_is_not_already_assigned(is_attribute_assigned, name)
        self._check_assign_argument_type(new_attribute, arg_type, name)
        if available_list is not None:
            self._check_if_assigned_object_is_in_available_list(new_attribute, available_list)

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, groups: Tuple[Group, ...]):
        self._check_if_assignment_is_available(self._attribute_assigned.groups,
                                               "Groups",
                                               groups,
                                               Group)
        self._groups = groups
        self._attribute_assigned.groups = groups
    
    @groups.deleter
    def groups(self):
        self._groups = None
        self._attribute_assigned.groups = False
        

    @property
    def assigned_lecturers(self):
        return self._assigned_lecturers

    @assigned_lecturers.setter
    def assigned_lecturers(self, lecturers: Tuple[Lecturer, ...]):
        self._check_if_assignment_is_available(self._attribute_assigned.lecturers,
                                               "Lecturers",
                                               lecturers,
                                               Lecturer,
                                               self.available_lecturers)
        self._assigned_lecturers = lecturers
        self._attribute_assigned.lecturers = bool(lecturers)

    @assigned_lecturers.deleter
    def assigned_lecturers(self):
        self._assigned_lecturers = None
        self._attribute_assigned.lecturers = False

    @property
    def assigned_rooms(self):
        return self._assigned_rooms

    @assigned_rooms.setter
    def assigned_rooms(self, rooms: Tuple[Room, ...]):
        self._check_if_assignment_is_available(self._attribute_assigned.rooms,
                                               "Rooms",
                                               rooms,
                                               Room,
                                               self.available_rooms)
        self._assigned_rooms = rooms
        self._attribute_assigned.rooms = bool(rooms)

    @assigned_rooms.deleter
    def assigned_rooms(self):
        self._assigned_rooms = None
        self._attribute_assigned.rooms = False

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: Time):
        self._check_if_attribute_is_not_already_assigned(self._attribute_assigned.time, "Start time")
        self._check_assign_argument_type([start_time], Time, " Start time")
        end_time = start_time + self.duration
        check_if_time_is_available((start_time, end_time))
        self._start_time = start_time
        self._end_time = end_time
        self._attribute_assigned.time = bool(start_time)

    @start_time.deleter
    def start_time(self):
        self._start_time = None
        self._end_time = None
        self._attribute_assigned.time = False

    @property
    def end_time(self):
        return self._end_time

    def _check_correct_assignment(self):
        if not self._attribute_assigned.is_all_assigned():
            raise RuntimeError(f"An attempt to assign classes without assign: {self._attribute_assigned}")

    def assign(self,
               time: Time = None,
               rooms: Tuple[Room, ...] = None,
               lecturers: Tuple[Lecturer, ...] = None,
               groups: Tuple[Group, ...] = None):
        if lecturers is not None:
            self.assigned_lecturers = lecturers
        if rooms is not None:
            self.assigned_rooms = rooms
        if time is not None:
            self.start_time = time
        if groups is not None:
            self.groups = groups
        self._check_correct_assignment()

    def unassign(self):
        del self.assigned_lecturers
        del self.assigned_rooms
        del self.start_time
        del self.groups






