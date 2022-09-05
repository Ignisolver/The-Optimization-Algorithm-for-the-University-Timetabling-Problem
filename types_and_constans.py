from enum import Enum, auto


class ClassesType(Enum):
    LECTURE = auto()
    ELE_LECTURE = auto()
    EXERCISE = auto()
    ELE_EXERCISE = auto()
    SLOT = auto()
    HALF_EXERCISE = auto()
    HALF_ELE_EXERCISE = auto()
    HALF_LECTURE = auto()
    HALF_ELE_LECTURE = auto()


class RoomId(str):
    pass


class BuildingId(str):
    pass

