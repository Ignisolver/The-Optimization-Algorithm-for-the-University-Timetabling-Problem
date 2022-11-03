from basic_structures.with_schedule import WithSchedule
from utils.types_ import GroupId


class Group(WithSchedule):
    def __init__(self, id_, name, amount_fo_students):
        super().__init__()
        self.id_: GroupId = id_
        self.name: str = name
        self.amount_of_students: int = amount_fo_students

    def __repr__(self):
        return self.name
