from typing import List, Tuple

from lecturer import Lecturer
from room import Room
from types_and_constans import ClassesType


class Classes:
    def __init__(self,
                 id_,
                 duration,
                 classes_type_: ClassesType,
                 available_rooms: Tuple[Room],
                 available_lecturers: Tuple[Lecturer]):
        self.id = id_
        self.duration = duration
        self.type = classes_type_
        self.available_rooms = available_rooms
        self.available_lecturer = available_lecturers
        self.groups = None
        self.assigned_lecturers = None
        self.assigned_rooms = None
        self.start_time = None
        self.end_time = None




