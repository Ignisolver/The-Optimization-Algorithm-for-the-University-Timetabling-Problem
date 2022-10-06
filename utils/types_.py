from dataclasses import dataclass
from enum import Enum


@dataclass
class ClassesType:
    LECTURE = 'LECTURE'
    LABORATORY = 'LABORATORY'


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
