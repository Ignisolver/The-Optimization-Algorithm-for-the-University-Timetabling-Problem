from typing import Dict, TYPE_CHECKING, List, Iterator

from data_generation.generation_configs import MAX_TIME_PER_DAY
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
        self._temp_dur = None
        self.assigned_classes_time: int = 0
        self.assigned_classes_amount: int = 0
        self.total_classes_time: int = 0
        self.total_classes_amount: int = 0
        self.over_doable: int = 0
        self.available_time: int = 0

    def __iter__(self) -> Iterator[DaySchedule]:
        return iter(self.days.values())

    def _set_unavailability(self, unavailability):
        if unavailability is not None:
            for unav_cl in unavailability:
                self.days[unav_cl.day].assign(unav_cl)

    def assign(self, classes: "Classes"):
        day_tag = classes.day
        self.days[day_tag].assign(classes)
        self.assigned_classes_time += int(classes.dur)
        self.assigned_classes_amount += 1

    def temp_assign(self, classes: "Classes"):
        self.temp_day_tag = classes.day
        self.days[self.temp_day_tag].temp_assign(classes)
        self.assigned_classes_time += int(classes.dur)
        self._temp_dur = int(classes.dur)
        self.assigned_classes_amount += 1

    def unassign_temp(self):
        self.days[self.temp_day_tag].unassign_temp()
        self.temp_day_tag = None
        self.assigned_classes_time -= self._temp_dur
        self.assigned_classes_amount -= 1

    def to_yaml(self):
        txt = ""
        for day_sche in self.days.values():
            for classes in day_sche:
                txt += classes.to_yaml() + "\n\n"
        return txt

    def calc_over_time_avail_time(self):
        all_avail_time = 5 * MAX_TIME_PER_DAY
        unav_time = sum(int(day.get_unavailable_len()) for day in self)
        self.available_time = all_avail_time - unav_time
        over_time = self.available_time - self.total_classes_time
        self.over_doable = -over_time

