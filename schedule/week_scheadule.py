from typing import Dict, TYPE_CHECKING

from schedule.day_scheadule import DaySchedule
from utils.constans import DAYS
from utils.types_ import Day

if TYPE_CHECKING:
    from basic_structures import Classes


class WeekSchedule:
    #todo add start unavailability mechanizm
    def __init__(self):
        self.days: Dict[Day, DaySchedule] = {day_tag: DaySchedule(day_tag)
                                             for day_tag in DAYS}
        self.temp_day_tag = None

    def assign(self, classes: "Classes"):
        day_tag = classes.day
        self.days[day_tag].assign(classes)

    def temp_assign(self, classes: "Classes"):
        self.temp_day_tag = classes.day
        self.days[self.temp_day_tag].temp_assign(classes)

    def unassign_temp(self):
        self.days[self.temp_day_tag].unassign_temp()
        self.temp_day_tag = None
