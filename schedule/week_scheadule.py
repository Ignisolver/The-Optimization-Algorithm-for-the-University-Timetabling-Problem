from typing import Dict, TYPE_CHECKING, Union, List

from schedule.day_scheadule import DaySchedule
from utils.constans import DAYS
from utils.types_ import Day

if TYPE_CHECKING:
    from basic_structures import Classes


class WeekSchedule:
    #todo add start unavailability mechanizm
    def __init__(self,
                 unavailability: Union[None, List["Classes"]] = None):
        self.days: Dict[Day, DaySchedule] = {day_tag: DaySchedule(day_tag)
                                             for day_tag in DAYS}
        self.temp_day_tag = None
        if unavailability is not None:
            self._set_unavailability(unavailability)

    def _set_unavailability(self, unavailability):
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
                txt += str(classes) + "\n\n"
        return txt
