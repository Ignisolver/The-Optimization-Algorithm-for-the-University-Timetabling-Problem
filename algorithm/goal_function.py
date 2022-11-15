"""
Funkcja celu - mierzy rozwiązanie:
1. czas przerw
- najlepszy = 0
- najgorszy = cały czas między zajęciami
2. Rozkład w dniu - ilość zajęć przed daną godziną - wagowo
- najlepiej = wszystko od rana
- najgorzej = wszystko wieczorem
3. Rozkład tygodniowy - ilość wykorzystanych dni
- najlepiej = minimalna ilość dni wykorzystana
- najgorzej = wszytskie dni wykorzystane
4. Równomierność - odchyłki od średniej optymalnej
- najlepiej = 0 różnic
- najgorzej = śrenia * 5
"""
from dataclasses import dataclass
from functools import cache
from itertools import cycle
from typing import Tuple, TYPE_CHECKING

from basic_structures import Classes
from data_generation.generation_configs import (MIN_HOUR,
                                                MAX_HOUR,
                                                WEEK_LENGTH_MIN,
                                                DAY_TIME_WEIGHTS,
                                                GOAL_FUNCTION_WEIGHTS as GFW,
                                                )
from schedule.week_scheadule import WeekSchedule
from utils.constans import BTW, WA, UNI, DU
from time_ import TimeDelta

if TYPE_CHECKING:
    from basic_structures.with_schedule import WithSchedule


class Metric:
    def __init__(self, week_schedule: WeekSchedule):
        self.ws = week_schedule
        self._best_brake_time = 0
        self._worst_brake_time = None
        self._worst_week_arrangement = 7
        self._classes_time = week_schedule.classes_time
        self._best_week_arrangement = 1
        self._medium_unfolding = None
        self._worst_uniformity = None
        self._best_uniformity = 0
        self._classes_amount = week_schedule.classes_amount
        self._best_days_unfolding = 0
        self._worst_days_unfolding = None
        self._calc_all_basics()

    def _calc_worst_brake_time(self):
        self._worst_brake_time = int(WEEK_LENGTH_MIN) - self._classes_time

    def _calc_medium_unfolding(self):
        self._medium_unfolding = int(self._classes_time /
                                     self._best_week_arrangement)

    def _calc_worst_uniformity(self):
        self._worst_uniformity = self._medium_unfolding * 5

    def _calc_worst_days_unfolding(self):

        day_obligatory_time = int(self._classes_time / 60 / 5) + 1
        points = 0
        for hour_n in range(1, day_obligatory_time + 1):
            points += DAY_TIME_WEIGHTS[-hour_n]
        self._worst_days_unfolding = points * 5

    def _calc_days_unfolding(self):
        points = 0
        for day in self.ws:
            for classes in day:
                points += DAY_TIME_WEIGHTS[classes.start_time.hour - MIN_HOUR.hour] + classes.start_time.minute/60
        return ((points - self._best_days_unfolding) /
                self._worst_days_unfolding)

    def _calc_brake_time_value(self):
        total_break_time = TimeDelta(0)
        for day in self.ws:
            total_break_time += day.get_brake_time(move_time_enable=False)
        return ((int(total_break_time) - self._best_brake_time) /
                self._worst_brake_time)

    def _calc_week_arrangement(self):
        n = 0
        for day in self.ws:
            if len(day.get_classes()) > 0:
                n += 0.2
        return n

    def _calc_uniformity(self):
        value = 0
        for day in self.ws:
            value += abs(len(day) - self._medium_unfolding)**2
        value = value**(1/2)
        return (value - self._best_uniformity) / self._worst_uniformity

    def _calc_all_basics(self):
        self._calc_worst_brake_time()
        self._calc_medium_unfolding()
        self._calc_worst_uniformity()
        self._calc_worst_days_unfolding()

    def calc_goal_fcn(self):
        btw = self._calc_brake_time_value() * GFW[BTW]
        wa = self._calc_week_arrangement() * GFW[WA]
        uni = self._calc_uniformity() * GFW[UNI]
        du = self._calc_days_unfolding() * GFW[DU]
        total_sum = btw + wa + uni + du
        return total_sum


# testme
def evaluate(items: Tuple["WithSchedule"]):
    val = 0
    for item in items:
        m = Metric(item.week_schedule)
        val += m.calc_goal_fcn()
    return val

