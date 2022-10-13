from basic_structures.with_schedule import WithSchedule
from utils.types_ import LecturerId


class Lecturer(WithSchedule):
    def __init__(self, id_, name):
        super().__init__()
        self.id_: LecturerId = id_
        self.name: str = name


class UnavailableLecturer():
    def __new__(cls, *args, **kwargs):
        return Lecturer(-1, "UNAVAILABLE")


