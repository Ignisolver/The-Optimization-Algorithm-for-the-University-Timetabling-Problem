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
from math import ceil
from statistics import mean
from typing import Tuple, TYPE_CHECKING

from data_generation.generation_configs import (MIN_HOUR,
                                                WEEK_LENGTH_MIN,
                                                DAY_TIME_WEIGHTS,
                                                GOAL_FUNCTION_WEIGHTS as GFW,
                                                MAX_TIME_PER_DAY,
                                                DURATIONS_OF_CLASSES,
                                                )
from schedule.week_scheadule import WeekSchedule
from utils.constans import BTW, WA, UNI, DU
from time_ import TimeDelta

if TYPE_CHECKING:
    from basic_structures.with_schedule import WithSchedule


@dataclass
class GFV:
    btw: float
    wa: float
    uni: float
    du: float

    def __add__(self, other):
        self.btw += other.btw
        self.wa += other.wa
        self.uni += other.uni
        self.du += other.du
        return self

    def __truediv__(self, other):
        self.btw = round(self.btw / other,1)
        self.wa = round(self.wa / other,1)
        self.uni = round(self.uni / other,2)
        self.du = round(self.du / other,2)
        return self

    def __iter__(self):
        return iter([self.btw, self.wa, self.uni, self.du])

    def __repr__(self):
        return (f"MEDIUM BREAK TIME     : {self.btw} hours\n" +
        f"MEDIUM BUSY DAYS      : {self.wa} \n" +
        f"MEDIUM UNIFORMITY     : {self.uni}\n" +
        f"MEDIUM DAYS UNFOLDING : {self.du}\n")

    def __mul__(self, gtw):
        self.btw *= gtw[BTW]
        self.wa *= gtw[WA]
        self.uni *= gtw[UNI]
        self.du *= gtw[DU]
        return self


class Metric:
    _mean_day_time_weights = mean(DAY_TIME_WEIGHTS)
    _longest_classes = max(DURATIONS_OF_CLASSES)

    def __init__(self, week_schedule: WeekSchedule):
        self.ws = week_schedule
        self._best_brake_time = 0
        self._worst_brake_time = None
        self._worst_week_arrangement = 7
        self._classes_time = week_schedule.total_classes_time
        self._best_week_arrangement = 1
        self._medium_unfolding = None
        self._worst_uniformity = None
        self._best_uniformity = 0
        self._classes_amount = week_schedule.assigned_classes_amount
        self._best_days_unfolding = 0
        self._worst_days_unfolding = None
        self._calc_all_basics()

    def _calc_worst_brake_time(self):
        self._worst_brake_time = int(WEEK_LENGTH_MIN) - self._classes_time

    def _calc_best_week_arrangement(self):
        div = self._classes_time / MAX_TIME_PER_DAY
        c_div = ceil(div)
        if c_div - div <= self._longest_classes:
            self._best_week_arrangement = c_div + 1
        else:
            self._best_week_arrangement = c_div

    def _calc_medium_unfolding(self):
        self._medium_unfolding = int(self._classes_time /
                                     self._best_week_arrangement)

    def _calc_worst_uniformity(self):
        self._worst_uniformity = self._medium_unfolding * 5

    def _calc_worst_days_unfolding(self):

        day_obligatory_time = ceil(self._classes_time / 60 / 5)
        points = 0
        for hour_n in range(1, day_obligatory_time + 1):
            points += DAY_TIME_WEIGHTS[-hour_n]
        self._worst_days_unfolding = points * 5

    def _calc_days_unfolding(self):
        points = 0
        for day in self.ws:
            for classes in day:
                points += DAY_TIME_WEIGHTS[classes.start_time.hour - MIN_HOUR.hour] + classes.start_time.minute/60
        points = points / self._mean_day_time_weights
        return points

    def _calc_brake_time_value(self):
        total_break_time = TimeDelta(0)
        for day in self.ws:
            total_break_time += day.get_brake_time(move_time_enable=False)
        return int(total_break_time)/60

    def _calc_week_arrangement(self):
        n = 0
        for day in self.ws:
            if len(day.get_classes()) > 0:
                n += 1
        return n

    def _calc_uniformity(self):
        value = 0
        counter_len_0 = -1
        for day in reversed(list(self.ws)):
            len_ = len(day.get_classes())
            if len_ != 0:
                value += (len(day) - self._medium_unfolding)**2
            elif len_ == 0:
                counter_len_0 += 1
                if counter_len_0 >= 5 - self._best_week_arrangement:
                    value += (len(day) - self._medium_unfolding) ** 2
        value = value**(1/2)
        return value

    def _calc_all_basics(self):
        self._calc_worst_brake_time()
        self._calc_best_week_arrangement()
        self._calc_medium_unfolding()
        self._calc_worst_uniformity()
        self._calc_worst_days_unfolding()

    def calc_goal_function_elements(self):
        btw = self._calc_brake_time_value()
        wa = self._calc_week_arrangement()
        uni = self._calc_uniformity()
        du = self._calc_days_unfolding()
        return GFV(btw, wa, uni, du)

    def calc_goal_fcn(self):
        total_sum = sum(self.calc_goal_function_elements()*GFW)
        return total_sum


def evaluate(items: Tuple["WithSchedule"]):
    val = 0
    for item in items:
        m = Metric(item.week_schedule)
        val += m.calc_goal_fcn()
    return val

