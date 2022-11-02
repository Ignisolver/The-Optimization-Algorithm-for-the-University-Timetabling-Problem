from dataclasses import dataclass, field
from typing import Dict, TYPE_CHECKING, Union

from basic_structures.with_schedule import WithSchedule
from utils.types_ import RoomId, ClassesId, UNAVAILABLE_ID

if TYPE_CHECKING:
    from classes import Classes


@dataclass
class Building:
    id_: int
    rooms: list = field(default_factory=list)


@dataclass
class Room(WithSchedule):
    id_: RoomId
    _initial_availability_minutes: int
    people_capacity: int = 0
    name: str = None
    build_id: int = None
    _curr_occup_min: int = 0
    _pred_occup: float = 0
    _classes_occup_probab: Dict[ClassesId, float] = \
        field(default_factory=dict)
    _const_classes_occup_probab: Dict[ClassesId, float] = \
        field(default_factory=dict)
    _occup_priority: float = 0  # the grater, the better
    _temp_cl: Union["Classes", None] = None

    def __post_init__(self):
        super().__init__()

    @property
    def occup_priority(self):
        if self._occup_priority == 0:
            raise RuntimeError("An attempt to get access to priority of"
                               " room for which all classes was assigned")
        else:
            return self._occup_priority

    def add_potential_classes(self, classes, probab=None):
        """
        use this function during initialisation step - before planning
        """
        if self._is_classes_available(classes.id_):
            raise RuntimeError("An attempt to add classes"
                               " again to the same room")
        if probab is None:
            probab = 1/len(classes.avail_rooms)
        self._classes_occup_probab[classes.id_] = probab
        self._const_classes_occup_probab[classes.id_] = probab
        self._update()

    def assign(self, classes: "Classes"):
        self._curr_occup_min += int(classes.dur)
        self._set_probab_of_classes(classes.id_, 0)
        super().assign(classes)

    def temp_assign(self, classes: "Classes"):
        self._curr_occup_min += int(classes.dur)
        self._set_probab_of_classes(classes.id_, 0)
        self._temp_cl = classes
        super(Room, self).temp_assign(classes)

    def unassign_temp(self):
        self._curr_occup_min -= int(self._temp_cl.dur)
        self._reset_probab_of_classes(self._temp_cl.id_)
        super(Room, self).unassign_temp()

    def _calc_priority(self):
        try:
            self._occup_priority = ((self._initial_availability_minutes -
                                     self._curr_occup_min) /
                                    self._pred_occup)
        except ZeroDivisionError:
            self._occup_priority = 0

    def _calc_predicted_occup(self):
        self._pred_occup = sum(self._classes_occup_probab.values())

    def _update(self):
        self._calc_predicted_occup()
        self._calc_priority()

    def _is_classes_available(self, classes_id) -> bool:
        return classes_id in self._classes_occup_probab.keys()

    def _set_probab_of_classes(self, classes_id: ClassesId, probab: float):
        """
        Use this function during planning
        """
        self._classes_occup_probab[classes_id] = probab
        self._update()

    def _reset_probab_of_classes(self, classes_id):
        probability = self._const_classes_occup_probab[classes_id]
        self._set_probab_of_classes(classes_id, probability)


class UnavailabilityRoom:
    def __new__(cls):
        return Room(id_=UNAVAILABLE_ID,
                    _initial_availability_minutes=0,
                    people_capacity=0,
                    name="NONE",
                    build_id=UNAVAILABLE_ID)
