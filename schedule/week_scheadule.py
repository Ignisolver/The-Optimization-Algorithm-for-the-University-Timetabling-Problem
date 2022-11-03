from typing import Dict, TYPE_CHECKING, List, Iterator

from schedule.day_scheadule import DaySchedule
from utils.constans import DAYS
from utils.types_ import Day

if TYPE_CHECKING:
    from basic_structures import Classes


class WeekSchedule:
    def __init__(self,
                 unavailability: None | List["Classes"] = None):
        self.days: Dict[Day, DaySchedule] = {day_tag: DaySchedule(day_tag)
                                             for day_tag in DAYS}
        self._set_unavailability(unavailability)
        self.temp_day_tag = None
        self.classes_time: int = 0
        self.classes_amount: int = 0

    def __iter__(self) -> Iterator[DaySchedule]:
        return iter(self.days.values())

    def _set_unavailability(self, unavailability):
        if unavailability is not None:
            for unav_cl in unavailability:
                self.days[unav_cl.day].assign(unav_cl)

    def assign(self, classes: "Classes"):
        day_tag = classes.day
        self.days[day_tag].assign(classes)

    def temp_assign(self, classes: "Classes"):
        self.temp_day_tag = classes.day
        self.days[self.temp_day_tag].temp_assign(classes)

    def unassign_temp(self):
        self.days[self.temp_day_tag].unassign_temp()
        self.temp_day_tag = None

    def to_yaml(self):
        txt = ""
        for day_sche in self.days.values():
            for classes in day_sche:
                txt += classes.to_yaml() + "\n\n"
        return txt
