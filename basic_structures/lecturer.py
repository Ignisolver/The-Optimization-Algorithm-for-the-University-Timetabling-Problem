from basic_structures.with_schedule import WithSchedule
from utils.types_ import LecturerId


class Lecturer(WithSchedule):
    def __init__(self, id_, name):
        super().__init__()
        self.id_: LecturerId = id_
        self.name: str = name

    def __eq__(self, other):
        if self.id_ == other.id_:
            return True
        else:
            return False

    def __repr__(self):
        return f"Lecturer(id:{self.id_}, name:{self.name})"

    def __hash__(self):
        return hash(self.id_)


class UnavailableLecturer():
    def __new__(cls, *args, **kwargs):
        return Lecturer(-1, "UNAVAILABLE")
