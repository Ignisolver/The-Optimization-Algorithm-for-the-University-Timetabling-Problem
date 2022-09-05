from dataclasses import dataclass
from typing import List, Tuple, Iterable, Type

from group import Group
from lecturer import Lecturer
from room import Room
from time_ import Time, TimeDelta
from types_ import ClassesType, ClassesId
from utils import check_type_all, check_if_time_is_available
from collections import namedtuple

Assignation = namedtuple("Assignation", ("lecturers", "groups", "rooms", "time"))


@dataclass
class Classes:
    id: ClassesId
    name: str
    duration: TimeDelta
    classes_type: ClassesType
    available_rooms: Tuple[Room, ...]
    available_lecturers: Tuple[Lecturer, ...]
    groups: Tuple[Group, ...] = None
    assigned_lecturers: Tuple[Lecturer, ...] = None
    assigned_rooms: Tuple[Room, ...] = None
    start_time: Time = None
    end_time: Time = None
    attribute_assigned = Assignation(False, False, False, False)

    @staticmethod
    def _check_if_attribute_is_not_already_assigned(attribute, name):
        if attribute is not None:
            raise RuntimeError(f"{name} already assigned")

    @staticmethod
    def _check_argument_type(argument: Iterable,
                             type_: Type,
                             name: str):
        if not check_type_all(argument, type_):
            raise ValueError(f"Argument is not {name}: {argument}")

    @staticmethod
    def _check_if_assigned_is_in_available(assigned, available):
        if not all(map(lambda x: x in available, assigned)):
            raise ValueError(f"Trying to assign unavailable object: {assigned} not in {available}")

    def assign_lecturers(self, lecturers: Tuple[Lecturer, ...]):
        name = "Lecturers"
        self._check_if_attribute_is_not_already_assigned(self.assigned_lecturers, name)
        self._check_argument_type(lecturers, Lecturer, name)
        self._check_if_assigned_is_in_available(lecturers, self.available_lecturers)
        self.assigned_lecturers = lecturers
        self.attribute_assigned.lecturers = True

    def assign_groups(self, groups: Tuple[Group, ...]):
        name = "Groups"
        self._check_if_attribute_is_not_already_assigned(self.groups, name)
        self._check_argument_type(groups, Group, name)
        self.groups = groups
        self.attribute_assigned.group = True

    def assign_rooms(self, rooms: Tuple[Room, ...]):
        name = "Rooms"
        self._check_if_attribute_is_not_already_assigned(self.assigned_rooms, name)
        self._check_argument_type(rooms, Room, name)
        self._check_if_assigned_is_in_available(rooms, self.available_rooms)
        self.assigned_rooms = rooms
        self.attribute_assigned.rooms = True

    def assign_time(self, start_time: Time):
        self._check_if_attribute_is_not_already_assigned(self.start_time, "Start time")
        self._check_if_attribute_is_not_already_assigned(self.end_time, "End time")
        self._check_argument_type([start_time], Time, " Start time")
        end_time = start_time + self.duration
        check_if_time_is_available((start_time, end_time))
        self.start_time = start_time
        self.end_time = end_time
        self.attribute_assigned.time = True

    def _check_correct_assignment(self):
        if not all(self.attribute_assigned):
            raise RuntimeError(f"An attempt to assign classes without assign: {self.attribute_assigned}")

    def assign(self,
               time: Time = None,
               rooms: Tuple[Room, ...] = None,
               lecturers: Tuple[Lecturer, ...] = None,
               groups: Tuple[Group, ...] = None):
        if lecturers is not None:
            self.assign_lecturers(lecturers)
        if rooms is not None:
            self.assign_rooms(rooms)
        if time is not None:
            self.assign_time(time)
        if groups is not None:
            self.assign_groups(groups)
        self._check_correct_assignment()

    def unassign(self):
        ...


# todo unnassign classes
# todo room manage priority
# todo update tests






