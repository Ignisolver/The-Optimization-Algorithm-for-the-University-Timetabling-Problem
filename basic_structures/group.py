from basic_structures.assignable import Assignable
from utils.types_ import GroupId


class Group(Assignable):
    def __init__(self, id_, name, amount_fo_students):
        self.id_: GroupId = id_
        self.name: str = name
        self.amount_of_students: int = amount_fo_students




