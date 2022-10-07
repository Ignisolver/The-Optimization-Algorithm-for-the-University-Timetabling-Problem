from typing import TYPE_CHECKING

from schedule.week_scheadule import WeekSchedule

if TYPE_CHECKING:
    from basic_structures import Classes


class WithSchedule:
    def __init__(self):
        self.week_schedule: WeekSchedule = WeekSchedule()

    def temp_assign(self, classes: "Classes"):
        self.week_schedule.temp_assign(classes)

    def unassign_temp(self):
        self.week_schedule.unassign_temp()

    def assign(self, classes: "Classes"):
        self.week_schedule.assign(classes)
