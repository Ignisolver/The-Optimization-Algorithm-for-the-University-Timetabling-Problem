from typing import List, Tuple, Iterable, Type

from group import Group
from lecturer import Lecturer
from room import Room
from time_ import Time
from types_ import ClassesType
from utils import check_type_all, check_if_time_is_available


class Classes:
    def __init__(self,
                 id_,
                 duration,
                 classes_type_: ClassesType,
                 available_rooms: Tuple[Room, ...],
                 available_lecturers: Tuple[Lecturer, ...]):
        self.id = id_
        self.duration = duration
        self.type = classes_type_
        self.available_rooms = available_rooms
        self.available_lecturers = available_lecturers
        self.groups = None
        self.assigned_lecturers = None
        self.assigned_rooms = None
        self.start_time = None
        self.end_time = None

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

    def assign_groups(self, groups: Tuple[Group, ...]):
        name = "Groups"
        self._check_if_attribute_is_not_already_assigned(self.groups, name)
        self._check_argument_type(groups, Group, name)
        self.groups = groups

    def assign_rooms(self, rooms: Tuple[Room, ...]):
        name = "Rooms"
        self._check_if_attribute_is_not_already_assigned(self.assigned_rooms, name)
        self._check_argument_type(rooms, Room, name)
        self._check_if_assigned_is_in_available(rooms, self.available_rooms)
        self.assigned_rooms = rooms

    def assign_time(self, start_time: Time):
        self._check_if_attribute_is_not_already_assigned(self.start_time, "Start time")
        self._check_if_attribute_is_not_already_assigned(self.end_time, "End time")
        self._check_argument_type([start_time], Time, " Start time")
        end_time = start_time + self.duration
        check_if_time_is_available((start_time, end_time))
        self.start_time = start_time
        self.end_time = end_time

    def assign(self):
        pass




