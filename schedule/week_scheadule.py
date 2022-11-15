from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING, List, Iterator

from data_generation.generation_configs import MAX_TIME_PER_DAY
from schedule.day_scheadule import DaySchedule
from utils.constans import DAYS
from utils.types_ import Day

if TYPE_CHECKING:
    from basic_structures import Classes


@dataclass
class FinalInfo:
    total_classes_len: int
    assigned_classes_len: int
    available_time_len: int


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

    def get_final_info(self) -> FinalInfo:
        unav_len = sum(int(day.get_unavailable_len()) for day in self)
        avail_time_len = 5 * MAX_TIME_PER_DAY - unav_len
        classes_len = sum(len(day) for day in self)
        fi = FinalInfo(self.classes_time,classes_len, avail_time_len)
        return fi
