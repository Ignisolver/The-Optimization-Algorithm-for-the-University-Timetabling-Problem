from dataclasses import dataclass, field
from typing import Dict, TYPE_CHECKING
from types_ import RoomId, ClassesId
from week_scheadule import WeekSchedule

if TYPE_CHECKING:
    from classes import Classes


@dataclass
class Room:
    id: RoomId
    place_capacity: int = 0
    schedule = WeekSchedule()

    def add_classes_to_room(self, classes_id):
        """
        use this function during initialisation step - before planning
        """
        self._occupation_probability_by_classes[classes_id] = None
        self._const_occupation_probability_by_classes[classes_id] = None

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

    def set_probability_of_classes(self,
                                   classes_id: ClassesId,
                                   probability: float):
        """
        Use this function during planning
        :param probability: probability that this classes will take place in this room
        """
        if classes_id not in self._occupation_probability_by_classes.keys():
            raise RuntimeError("An attempt to access to not existing classes")
        self._occupation_probability_by_classes[classes_id] = probability
        self._const_occupation_probability_by_classes[classes_id] = probability
        self._update()

    def assign(self, classes: "Classes"):
        self.set_probability_of_classes(classes.id, 0)
        self._current_occupation += int(classes.duration)
        self.schedule.assign(classes)

    def unassign(self, classes: "Classes"):
        self.set_probability_of_classes(classes.id, )
        self._current_occupation -= int(classes.duration)
        self.schedule.unassign(classes)


@dataclass
class PriorityManager:
    _current_occupation: int = 0
    _occupation_probability: float = 0
    _occupation_probability_by_classes: Dict[ClassesId, float] = field(default_factory=dict)
    _const_occupation_probability_by_classes: Dict[ClassesId, float] = field(default_factory=dict)
    priority: float = 0