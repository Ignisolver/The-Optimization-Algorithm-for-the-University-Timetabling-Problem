from dataclasses import dataclass


@dataclass
class ClassesType:
    LECTURE = 'LECTURE'
    LABORATORY = 'LABORATORY'
    UNAVAILABLE = "UNAVAILABLE"


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


class Building(list):
    pass


class TimeRangeType:
    pass


UNAVAILABLE_ID = -1

COLORS = ['edc9cd', '1d6c2b', '1f08b0', 'a3c1ad', 'e35259', '22b4b7', '4d5d53', 'bcbbff', '4d5d53', '96c8a2',
          'efdfbb', '8fbc8f', 'bdb76b', 'fffdd0', 'eee8cd', '8c92ac', 'f7e7ce', 'ace1af', '78866b', 'a3c1ad',
          '669999', 'eeeed1', 'd8d1b0', '090088', 'c6c1b9', '003da6', '362d17', '01e1ec', '5e8d63', '002060',
          'ffc000', '54d157', 'ff9400', 'c22c4e', '5faca1', 'b1044f', '541d8b', 'e82cb5', '14b437', '7a0c72',
          '79eb00', '412c39']


def _color_getter():
    while True:
        for color in COLORS:
            yield color


DAY_LETTER = dict(zip(range(7), ("M","T","W","R","F","Sa", "Su")))

get_color = _color_getter()

