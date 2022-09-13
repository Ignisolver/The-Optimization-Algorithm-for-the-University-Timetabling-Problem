from dataclasses import dataclass
from enum import Enum


class InputStructureType(Enum):
    Room = "Room"
    Lecturer = "Lecturer"
    Group = "Group"
    Classes = "Classes"


@dataclass
class Tag:
    TYPE = "TYPE"
    ID = "ID"
    NAME = "NAME"
    AMOUNT_OF_STUDENTS = "AMOUNT_OF_STUDENTS"
    CLASSES_TO_ASSIGN = "CLASSES_TO_ASSIGN"
    AVAILABLE_TIMES = "AVAILABLE_TIMES"
    UNAVAILABLE_TIMES = "UNAVAILABLE_TIMES"
    DURATION = "DURATION"
    CLASSES_TYPE = "CLASSES_TYPE"
    AVAILABLE_ROOMS = "AVAILABLE_ROOMS"
    GROUPS = "GROUPS"
    LECTURERS = "LECTURERS"
    PREFERRED_TIMES = "PREFERRED_TIMES"
    CAPACITY = "CAPACITY"



