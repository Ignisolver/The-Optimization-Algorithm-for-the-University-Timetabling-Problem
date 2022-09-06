from dataclasses import dataclass, field
from typing import Dict, TYPE_CHECKING
from types_ import RoomId, ClassesId
from week_scheadule import WeekSchedule

if TYPE_CHECKING:
    from classes import Classes


@dataclass
class Room:
    id_: RoomId
    _initial_availability_minutes: int
    people_capacity: int = 0
    schedule: WeekSchedule = field(default_factory=WeekSchedule)
    _current_occupation_minutes: int = 0
    _predicted_occupation: float = 0
    _classes_occupation_probability: Dict[ClassesId, float] = field(default_factory=dict)
    _const_classes_occupation_probability: Dict[ClassesId, float] = field(default_factory=dict)
    _occupation_priority: float = 0  # the grater, the better

    @property
    def occupation_priority(self):
        if self._occupation_priority == 0:
            raise RuntimeError("An attempt to get access to priority of room for which all classes was assigned")
        else:
            return self._occupation_priority

    def _calc_priority(self):
        try:
            self._occupation_priority = (self._initial_availability_minutes - self._current_occupation_minutes) / \
                                        self._predicted_occupation
        except ZeroDivisionError:
            self._occupation_priority = 0

    def _calc_predicted_occupation(self):
        self._predicted_occupation = sum(self._classes_occupation_probability.values())

    def _update(self):
        self._calc_predicted_occupation()
        self._calc_priority()

    def add_new_potential_classes_to_room(self, classes, probability):
        """
        use this function during initialisation step - before planning
        """
        if self._is_classes_available(classes.id_):
            raise RuntimeError("An attempt to add classes again to the same room")
        self._classes_occupation_probability[classes.id_] = probability
        self._const_classes_occupation_probability[classes.id_] = probability
        self._update()

    def _is_classes_available(self, classes_id):
        return classes_id in self._classes_occupation_probability.keys()

    def _set_probability_of_classes(self,
                                    classes_id: ClassesId,
                                    probability: float):
        """
        Use this function during planning
        """
        if not self._is_classes_available(classes_id):
            raise RuntimeError("An attempt to access to not existing classes")
        self._classes_occupation_probability[classes_id] = probability
        self._update()

    def _reset_probability_of_classes(self, classes_id):
        probability = self._const_classes_occupation_probability[classes_id]
        self._set_probability_of_classes(classes_id, probability)

    def assign(self, classes: "Classes"):
        self._current_occupation_minutes += int(classes.duration)
        self._set_probability_of_classes(classes.id_, 0)
        self.schedule.assign(classes)

    def unassign(self, classes: "Classes"):
        self._current_occupation_minutes -= int(classes.duration)
        self._reset_probability_of_classes(classes.id_)
        self.schedule.unassign(classes)