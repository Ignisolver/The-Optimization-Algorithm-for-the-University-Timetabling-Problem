from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class ClassesTypes:
    LECTURE = 'LECTURE'
    LABOLATORY = 'LABOLATORY'
    ELECTIVE = 'ELECTIVE'
    NORMAL = 'NORMAL'


class ClassesType:
    def __init__(self, init_str: str):
        le_la, el_no, weeks = init_str.split('-')
        if le_la == "W":
            self.lect_lab = ClassesTypes.LECTURE
        elif le_la == "L":
            self.lect_lab = ClassesTypes.LABOLATORY
        else:
            raise ValueError(f"Incorrect classes type {init_str}")
        if el_no == "E":
            self.el_no = ClassesTypes.ELECTIVE
        elif el_no == "N":
            self.el_no = ClassesTypes.NORMAL
        else:
            raise ValueError(f"Incorrect classes type {init_str}")
        self.weeks = int(weeks)


class RoomId(int):
    pass


class LecturerId(int):
    pass


class GroupId(int):
    pass


class ClassesId(int):
    pass


class BuildingId(str):
    pass


class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Week(int):
    pass


class TimeType:
    pass


class TimeRangeType:
    pass
