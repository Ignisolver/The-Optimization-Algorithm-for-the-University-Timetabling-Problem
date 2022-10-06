from basic_structures.assignable import Assignable
from utils.types_ import LecturerId


class Lecturer(Assignable):
    def __init__(self, id_, name):
        self.id_: LecturerId = id_
        self.name: str = name


