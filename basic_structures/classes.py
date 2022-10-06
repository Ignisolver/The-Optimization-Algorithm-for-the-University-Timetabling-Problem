from dataclasses import dataclass
from typing import Tuple, Union

from basic_structures.group import Group
from basic_structures.lecturer import Lecturer
from basic_structures.room import Room
from time_ import Time, TimeDelta
from utils.types_ import ClassesType, ClassesId


@dataclass
class Classes:
    #todo testme
    id_: ClassesId
    name: str
    dur: TimeDelta
    classes_type: ClassesType
    avail_rooms: Tuple[Room, ...]
    lecturer: Lecturer
    groups: Tuple[Group]
    assigned_room: Room | None = None
    _start_time: Union[Time, None] = None
    _end_time: Union[Time, None] = None

    def assign(self,
               time: Time = None,
               room: Room = None):
        if room is not None:
            self.assigned_room = room
        if time is not None:
            self.start_time = time

    def unassign(self):
        del self.assigned_room
        del self.start_time

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @start_time.setter
    def start_time(self, start_time: Time):
        end_time = start_time + self.dur
        self._start_time = start_time
        self._end_time = end_time

    @start_time.deleter
    def start_time(self):
        self._start_time = None
        self._end_time = None
    
    def pretty_represent(self):
        id_ = f"{self.id_:>5}"
        start_time = f"{self.start_time.hour:>02}:{self.start_time.minute:>02}"
        end_time = f"{self.end_time.hour:>02}:{self.end_time.minute:>02}"
        name = f"{self.name}"
        type_ = self.classes_type
        s1 = f"{id_} | {start_time} -> {end_time} | "
        s2 = f"{type_:>10} | {name}"
        print(s1 + s2)

