from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple, Iterable, Union, List

from basic_structures.group import Group
from basic_structures.lecturer import Lecturer
from basic_structures.room import Room
from time_ import Time, TimeDelta
from utils.none_machine import NM
from utils.types_ import ClassesType, ClassesId, ClassesTypes
from utils.utils import check_type_all, check_if_time_is_available


class AttrName(Enum):
    LECT = "Lecturer"
    ROOM = "Room"
    TIME = "Time"
    GROUP = "Group"

Attr = namedtuple("Attr",("val", "type"))

@dataclass
class ValType:
    val: bool
    type: type


@dataclass
class Assignation:
    #testme
    def __init__(self):
        self._attrs = {AttrName.LECT: ValType(False, Lecturer),
                       AttrName.ROOM: ValType(False, Room),
                       AttrName.GROUP: ValType(False, Group),
                       AttrName.TIME: ValType(False, Time)}

    def __iter__(self):
        return iter(el.val for el in self._attrs.values())

    def __getitem__(self, item):
        return self._attrs[item]

    def __setitem__(self, key, value):
        self._attrs[key].val = value

# todo multi lecturer, group, room, classes
# todo przypisywanie do każdego elementu w środku podczas przypisywania zajęć
#  - po dodaniu multi...


@dataclass
class Classes:
    id_: ClassesId
    name: str
    dur: TimeDelta
    classes_type: ClassesType
    avail_rooms: Tuple[Room, ...]
    avail_lecturers: Tuple[Lecturer, ...]
    _groups: Union[Tuple[Group, ...], None] = None
    _assigned_lecturers: Union[Tuple[Lecturer, ...], None] = None
    _assigned_rooms: Union[Tuple[Room, ...], None] = None
    _start_time: Union[Time, None] = None
    _end_time: Union[Time, None] = None
    _attr_assigned: Assignation = field(default_factory=Assignation)

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
    def total_amount_of_students(self) -> Union[int, None]:
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
        self._assert_assignment_is_available(AttrName.GROUP, groups)
        self._groups = groups
        self._attr_assigned[AttrName.GROUP] = True

    @assigned_lecturers.setter
    def assigned_lecturers(self, lecturers: Tuple[Lecturer, ...]):
        self._assert_assignment_is_available(AttrName.LECT, lecturers,
                                             self.avail_lecturers)
        self._assigned_lecturers = lecturers
        self._attr_assigned[AttrName.LECT] = True

    @assigned_rooms.setter
    def assigned_rooms(self, rooms: Tuple[Room, ...]):
        self._assert_assignment_is_available(AttrName.ROOM, rooms,
                                             self.avail_rooms)
        self._assigned_rooms = rooms
        self._attr_assigned[AttrName.ROOM] = True

    @start_time.setter
    def start_time(self, start_time: Time):
        self._assert_attr_is_not_already_assigned(AttrName.TIME)
        end_time = start_time + self.dur
        check_if_time_is_available((start_time, end_time))
        self._start_time = start_time
        self._end_time = end_time
        self._attr_assigned[AttrName.TIME] = bool(start_time)

    @groups.deleter
    def groups(self):
        self._assert_attr_is_already_assigned(AttrName.GROUP)
        self._groups = None
        self._attr_assigned[AttrName.GROUP] = False

    @assigned_lecturers.deleter
    def assigned_lecturers(self):
        self._assert_attr_is_already_assigned(AttrName.LECT)
        self._assigned_lecturers = None
        self._attr_assigned[AttrName.LECT] = False

    @assigned_rooms.deleter
    def assigned_rooms(self):
        self._assert_attr_is_already_assigned(AttrName.ROOM)
        self._assigned_rooms = None
        self._attr_assigned[AttrName.ROOM] = False

    @start_time.deleter
    def start_time(self):
        self._assert_attr_is_already_assigned(AttrName.TIME)
        self._start_time = None
        self._end_time = None
        self._attr_assigned[AttrName.TIME] = False

    def _assert_correct_assignment(self):
        if not all(self._attr_assigned):
            raise RuntimeError(f"An attempt to assign classes "
                               f"without assign: {self._attr_assigned}")

    def _assert_attr_is_not_already_assigned(self, attr_name: AttrName):
        if self._attr_assigned[attr_name].val:
            raise RuntimeError(f"{attr_name.value} already assigned")

    def _assert_attr_is_already_assigned(self, attr_name: AttrName):
        if not self._attr_assigned[attr_name].val:
            raise RuntimeError(
                f"{attr_name.value} attribute is not assigned yet"
                f" - an attempt to unassign!")

    def _assert_correct_arg(self, arg: List,
                            arg_name: AttrName):
        arg_type = self._attr_assigned[arg_name].type
        if len(arg) == 0 or (not check_type_all(arg, arg_type)):
            raise ValueError(f"Argument invalid '{arg_name.value}': {arg}")

    @staticmethod
    def _assert_is_in_available_list(obj, available):
        if not all(map(lambda x: x in available, obj)):
            raise ValueError(f"Trying to assign unavailable object:"
                             f" {obj} not in {available}")

    def _assert_assignment_is_available(self, attr_name: AttrName,
                                        new_attribute, available_list=None):
        self._assert_attr_is_not_already_assigned(attr_name)
        self._assert_correct_arg(new_attribute, attr_name)
        if available_list is not None:
            self._assert_is_in_available_list(new_attribute, available_list)

    @staticmethod
    def _assert_rooms_are_able_to_hold_groups(groups: Iterable[Group],
                                              rooms: Iterable[Room]):
        amount_of_student_in_groups = sum(g.amount_of_students for g in groups)
        capacity_in_rooms = sum(room.people_capacity for room in rooms)
        if capacity_in_rooms < amount_of_student_in_groups:
            raise RuntimeError("There is no enough space"
                               " for all groups in rooms")

    @staticmethod
    def _assert_correct_usage(n_r, n_g):
        if NM.both_nones(n_r, n_g):
            raise RuntimeError("Invalid usage of function")
        # testme

    def _assert_rooms_and_groups_input_correctness(self, new_groups=None,
                                                   new_rooms=None):
        self._assert_correct_usage(new_rooms, new_groups)

        if NM.both_not_none(self.assigned_rooms, new_groups):
            self._assert_rooms_are_able_to_hold_groups(new_groups,
                                                       self.assigned_rooms)
        if NM.both_not_none(self.groups, new_rooms):
            self._assert_rooms_are_able_to_hold_groups(self.groups, new_rooms)

        if (NM.both_not_none(new_groups, new_rooms) and
                NM.both_nones(self.groups, self.assigned_rooms)):
            self._assert_rooms_are_able_to_hold_groups(new_groups, new_rooms)
    
    def pretty_represent(self):
        id_ = f"{self.id_:>5}"
        start_time = f"{self.start_time.hour:>02}:{self.start_time.minute:>02}"
        end_time = f"{self.end_time.hour:>02}:{self.end_time.minute:>02}"
        name = f"{self.name}"
        type_ = self.classes_type
        s1 = f"{id_} | {start_time} -> {end_time} | "
        s2 = f"{type_.el_no:<8}-{type_.lect_lab:>10} | {name}"
        print(s1 + s2)

