from dataclasses import dataclass, field

from typing import TYPE_CHECKING, Dict

from utils.types_ import GroupId, ClassesId
from schedule.week_scheadule import WeekSchedule

if TYPE_CHECKING:
    from classes import Classes


@dataclass
class Group:
    id_: GroupId
    amount_of_students: int
    name: str = None
    week_schedule: WeekSchedule = field(default_factory=WeekSchedule)
    _unassigned_classes: Dict[ClassesId, "Classes"] =\
        field(default_factory=dict)
    _assigned_classes: Dict[ClassesId, "Classes"] = field(default_factory=dict)

    def add_classes_to_assign(self, classes: "Classes"):
        self._assert_classes_not_in_available_unassigned(classes)
        self._assert_classes_not_in_assigned(classes)
        self._unassigned_classes[classes.id_] = classes

    def assign(self, classes: "Classes"):
        self._assert_classes_in_available_unassigned(classes)
        self._assert_classes_not_in_assigned(classes)
        self.week_schedule.assign(classes)
        self._move_classes_to_assigned(classes)

    def unassign(self, classes: "Classes"):
        self._assert_classes_not_in_available_unassigned(classes)
        self._assert_classes_in_assigned(classes)
        self.week_schedule.unassign(classes)
        self._move_classes_to_unassigned(classes)

    def _is_classes_in_assigned(self, classes: "Classes") -> bool:
        return classes.id_ in self._assigned_classes

    def _is_classes_in_available_unassigned(self, classes: "Classes") -> bool:
        return classes.id_ in self._unassigned_classes

    def _assert_classes_in_available_unassigned(self, classes: "Classes"):
        if not self._is_classes_in_available_unassigned(classes):
            raise RuntimeError(f"Classes: f{classes} unavailable"
                               f" for group: {self}")

    def _assert_classes_not_in_available_unassigned(self, classes: "Classes"):
        if self._is_classes_in_available_unassigned(classes):
            raise RuntimeError(f"Classes: f{classes} already added "
                               f"for group: {self}")

    def _assert_classes_in_assigned(self, classes):
        if not self._is_classes_in_assigned(classes):
            raise RuntimeError(f"Classes: {classes} is not assigned")

    def _assert_classes_not_in_assigned(self, classes):
        if self._is_classes_in_assigned(classes):
            raise RuntimeError(f"Classes: {classes} is already assigned")

    def _move_classes_to_assigned(self, classes):
        del self._unassigned_classes[classes.id_]
        self._assigned_classes[classes.id_] = classes

    def _move_classes_to_unassigned(self, classes):
        del self._assigned_classes[classes.id_]
        self._unassigned_classes[classes.id_] = classes

