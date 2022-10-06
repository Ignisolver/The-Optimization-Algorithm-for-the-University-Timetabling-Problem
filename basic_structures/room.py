from dataclasses import dataclass, field
from typing import Dict, TYPE_CHECKING

from basic_structures.assignable import Assignable
from utils.types_ import RoomId, ClassesId

if TYPE_CHECKING:
    from classes import Classes


@dataclass
class Room(Assignable):
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

    def __post_init__(self):
        super().__init__()

    @property
    def occup_priority(self):
        if self._occup_priority == 0:
            raise RuntimeError("An attempt to get access to priority of"
                               " room for which all classes was assigned")
        else:
            return self._occup_priority

    def add_potential_classes(self, classes, probab):
        """
        use this function during initialisation step - before planning
        """
        if self._is_classes_available(classes.id_):
            raise RuntimeError("An attempt to add classes"
                               " again to the same room")
        self._classes_occup_probab[classes.id_] = probab
        self._const_classes_occup_probab[classes.id_] = probab
        self._update()

    def assign(self, classes: "Classes"):
        self._curr_occup_min += int(classes.dur)
        self._set_probab_of_classes(classes.id_, 0)
        super().assign(classes)

    def unassign(self, classes: "Classes"):
        self._curr_occup_min -= int(classes.dur)
        self._reset_probab_of_classes(classes.id_)
        super().unassign(classes)

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
        if not self._is_classes_available(classes_id):
            raise RuntimeError("An attempt to access to not existing classes")
        self._classes_occup_probab[classes_id] = probab
        self._update()

    def _reset_probab_of_classes(self, classes_id):
        probability = self._const_classes_occup_probab[classes_id]
        self._set_probab_of_classes(classes_id, probability)