from dataclasses import dataclass


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


class Day(int):
    pass


MONDAY = Day(0)
TUESDAY = Day(1)
WEDNESDAY = Day(2)
THURSDAY = Day(3)
FRIDAY = Day(4)
SATURDAY = Day(5)
SUNDAY = Day(6)


class Week(int):
    pass


class TimeType:
    pass


class TimeRangeType:
    pass
