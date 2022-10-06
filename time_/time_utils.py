from typing import TYPE_CHECKING, Union

from utils.constans import DAYS
from utils.none_machine import NM
from utils.types_ import Week, Day

if TYPE_CHECKING:
    from time_ import Time
    from time_ import TimeRange


class DateCorrectnessCaretaker:
    def assert_days_and_weeks_correctness(self, one_time: Union["Time",
                                                                "TimeRange"],
                                          another_time: Union["Time",
                                                              "TimeRange"],
                                          none_able=True):
        if none_able:
            if self._are_week_and_day_nones_in_one(one_time, another_time):
                return None
        self._assert_days_and_weeks_same(one_time, another_time)

    @staticmethod
    def _are_weeks_and_days_same(one_time, another_time):
        return ((one_time.day == another_time.day) and
                (one_time.week == another_time.week))

    @staticmethod
    def _are_day_and_week_set(day, week):
        return (day in DAYS) and isinstance(week, Week)

    @staticmethod
    def _are_week_and_day_nones_in_one(one_t: Union["Time", "TimeRange"],
                                       another_t: Union["Time", "TimeRange"]):
        return (NM.both_nones(one_t.day, one_t.week) or
                NM.both_nones(another_t.day, another_t.week))

    def _assert_days_and_weeks_same(self, one_time, another_time):
        if not self._are_weeks_and_days_same(one_time, another_time):
            raise RuntimeError(
                "Operation forbidden for times with different days")

    def assert_args_day_and_week_correct(self, day, week):
        if (NM.both_nones(day, week) or
                self._are_day_and_week_set(day, week)):
            pass
        else:
            raise RuntimeError(
                f"Day and week are not correct: Day: {day}; Week: {week}")
