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

from math import ceil

from data import (MIN_HOUR, MAX_HOUR, MAX_TIME_PER_DAY, DAY_TIME_WEIGHTS,
                  GOAL_FUNCTION_WEIGHTS as GFW)
from schedule.week_scheadule import WeekSchedule
from time_ import TimeDelta, TimeRange


def iterator_over_day():
    period = int((MAX_HOUR-MIN_HOUR) / len(DAY_TIME_WEIGHTS))
    start = MIN_HOUR
    end = MIN_HOUR + period
    weights = iter(DAY_TIME_WEIGHTS)
    while end <= MAX_HOUR:
        yield start, end, next(weights)
        start += period
        end += period


class Metric:
    #testme
    def __init__(self, week_schedule: WeekSchedule):
        self.ws = week_schedule
        self._best_brake_time = 0
        self._worst_brake_time = None
        self._worst_week_arrangement = 7
        self._classes_time = None
        self._best_week_arrangement = 0
        self._medium_unfolding = None
        self._worst_uniformity = None
        self._best_uniformity = 0
        self._classes_amount = 0
        self._best_days_unfolding = None
        self._worst_days_unfolding = None

    def _calc_worst_brake_time(self):
        self._worst_brake_time = TimeDelta(0)
        for day in self.ws:
            self._worst_brake_time += day.get_brake_time()

    def _calc_classes_time(self):
        for day in self.ws:
            self._classes_time += len(day)

    def _calc_best_week_arrangement(self):
        self._best_week_arrangement = ceil(self._classes_time /
                                           int(MAX_TIME_PER_DAY))

    def _calc_medium_unfolding(self):
        self._medium_unfolding = int(self._classes_time /
                                     self._best_week_arrangement)

    def _calc_worst_uniformity(self):
        self._worst_uniformity = self._medium_unfolding * 5

    def _calc_amount_of_classes(self):
        for day in self.ws:
            self._classes_amount += day.get_amount_of_classes()

    def _calc_best_days_unfolding(self):
        day_obligatory_time = int(self._classes_time /
                                  self._best_week_arrangement)
        day_obl_td = TimeDelta(0, day_obligatory_time)
        counted_time = TimeDelta(0, 0)
        points = 0
        for start, end, weight in iterator_over_day():
            td = TimeRange(start, end).dur
            if counted_time < day_obl_td:
                points += weight * self._best_week_arrangement
                counted_time += td
            else:
                break
        self._best_days_unfolding = points

    def _calc_worst_days_unfolding(self):
        day_obligatory_time = int(self._classes_time /
                                  self._best_week_arrangement)
        day_obl_td = TimeDelta(0, day_obligatory_time)
        counted_time = TimeDelta(0, 0)
        points = 0
        for start, end, weight in reversed(list(iterator_over_day())):
            td = TimeRange(start, end).dur
            if counted_time < day_obl_td:
                points += weight * self._best_week_arrangement
                counted_time += td
            else:
                break
        self._worst_days_unfolding = points

    def _calc_days_unfolding(self):
        points = 0
        for start_h, end_h, weight in iterator_over_day():
            for day in self.ws:
                cl_am = day.get_amount_of_classes_between(start_h, end_h)
                if cl_am > 0:
                    points += weight
        days_unfolding = points / self._classes_amount
        return ((days_unfolding - self._best_days_unfolding) /
                 self._best_days_unfolding)

    def _calc_brake_time_value(self):
        total_break_time = 0
        for day in self.ws:
            total_break_time += day.get_brake_time()
        return ((total_break_time - self._best_brake_time) /
                 self._worst_brake_time)

    def _calc_week_arrangement(self):
        n = 0
        for day in self.ws:
            if len(day.get_classes()) > 0:
                n += 1
        return (self._best_week_arrangement - n) / self._worst_week_arrangement

    def _calc_uniformity(self):
        value = 0
        for day in self.ws:
            value += abs(len(day) - self._medium_unfolding)
        return (value - self._best_uniformity ) / self._worst_uniformity

    def _calc_all_basics(self):
        self._calc_worst_brake_time()
        self._calc_classes_time()
        self._calc_best_week_arrangement()
        self._calc_medium_unfolding()
        self._calc_worst_uniformity()
        self._calc_amount_of_classes()
        self._calc_best_days_unfolding()
        self._calc_worst_days_unfolding()

    def calc_goal_fcn(self):
        self._calc_all_basics()
        btw = self._calc_brake_time_value() * GFW[0]
        wa = self._calc_week_arrangement() * GFW[1]
        unif = self._calc_uniformity() * GFW[2]
        du = self._calc_days_unfolding() * GFW[3]






















