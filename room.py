from dataclasses import dataclass, field
from typing import Dict, TYPE_CHECKING
from types_ import RoomId, ClassesId
from week_scheadule import WeekSchedule

if TYPE_CHECKING:
    from classes import Classes


@dataclass
class Room:
    id: RoomId
    capacity: int = 0
    _current_occupation: int = 0
    _initial_availability: int = 0
    _occupation_probability: float = 0
    _occupation_probability_by_classes: Dict[ClassesId, float] = field(default_factory=dict)
    priority: float = 0
    schedule = WeekSchedule()

    def _calc_priority(self):
        try:
            self.priority = (self._initial_availability - self._current_occupation) / self._predicted_occupation
        except ZeroDivisionError:
            self.priority = 0

    def _calc_predicted_occupation(self):
        self._predicted_occupation = sum(self._occupation_probability_by_classes.values())

    def _update(self):
        self._calc_predicted_occupation()
        self._calc_priority()

    def set_probability_by_classes(self,
                                   classes_id: ClassesId,
                                   probability: float):
        self._occupation_probability_by_classes[classes_id] = probability
        ...


    def _assign(self, classes: "Classes"):
        self._occupation_probability_by_classes[classes.id] = 0
        self._current_occupation += int(classes.duration)
        self._update()
        ...



