from typing import TYPE_CHECKING, Union

from utils.constans import DAYS
from utils.types_ import Week, Day

if TYPE_CHECKING:
    from time_ import Time
    from time_ import TimeRange


# todo add missing tests
class DateCorrectnessCaretaker:

    def assert_days_and_weeks_correctness(self, one_time: Union["Time", "TimeRange"],
                                          another_time: Union["Time", "TimeRange"],
                                          none_able=False):
        if none_able:
            if self._are_both_day_and_week_in_self_or_other_nones(one_time, another_time):
                return None
        self._assert_days_and_weeks_same(one_time, another_time)

    @staticmethod
    def _are_weeks_and_days_same(one_time, another_time):
        return (one_time.day == another_time.day) and (one_time.week == another_time.week)

    @staticmethod
    def _are_day_and_week_nones(day, week):
        return (day is None) and (week is None)

    @staticmethod
    def _are_day_and_week_set(day, week):
        return (day in DAYS) and isinstance(week, Week)

    def _are_both_day_and_week_in_self_or_other_nones(self,
                                                      one_time: Union["Time", "TimeRange"],
                                                      another_time: Union["Time", "TimeRange"]):
        return (self._are_day_and_week_nones(one_time.day, one_time.week) or
                self._are_day_and_week_nones(another_time.day, another_time.week))

    def _assert_days_and_weeks_same(self, one_time, another_time):
        if not self._are_weeks_and_days_same(one_time, another_time):
            raise RuntimeError("Operation forbidden for times with different days")

    def assert_initial_arguments_day_and_week_correct(self, day, week):
        if (self._are_day_and_week_nones(day, week) or
                self._are_day_and_week_set(day, week)):
            pass
        else:
            raise RuntimeError(f"Day and week are not correct: Day: {day}; Week: {week}")


