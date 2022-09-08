from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING

from utils.types_ import LecturerId, ClassesId
from schedule.week_scheadule import WeekSchedule

if TYPE_CHECKING:
    from classes import Classes


@dataclass
class Lecturer:
    id_: LecturerId
    week_schedule: WeekSchedule = field(default_factory=WeekSchedule)
    _available_classes: List[ClassesId] = field(default_factory=list)

    def _classes_is_available(self, classes: "Classes") -> bool:
        return classes.id_ in self._available_classes

    def _assert_classes_available(self, classes: "Classes"):
        if not self._classes_is_available(classes):
            raise RuntimeError("An attempt to assign unavailable classes to Lecturer")

    def _assert_new_classes(self, classes):
        if self._classes_is_available(classes):
            raise RuntimeError("An attempt to add already added classes to Lecturer")

    def add_available_classes(self, classes: "Classes"):
        self._assert_new_classes(classes)
        self._available_classes.append(classes.id_)

    def assign(self, classes: "Classes"):
        self._assert_classes_available(classes)
        self.week_schedule.assign(classes)

    def unassign(self, classes: "Classes"):
        self.week_schedule.assign(classes)

