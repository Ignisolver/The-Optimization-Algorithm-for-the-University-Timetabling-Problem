from typing import TYPE_CHECKING

from utils.constans import DAYS
from utils.types_ import Week

if TYPE_CHECKING:
    from time_ import Time
    from time_ import TimeRange


# todo add missing tests
class DateCorrectnessCaretaker:
    def assert_arguments_day_and_week_correct(self, day, week):
        self._assert_day_and_week_types_correctness(day, week)
        self._assert_day_and_week_are_both_set_or_both_none(day, week)

    def assert_days_and_weeks_correctness(self, one_time: "Time" or "TimeRange",
                                          another_time: "Time" or "TimeRange",
                                          none_able=False):
        if none_able:
            if self._is_day_and_week_in_self_or_other_nones(one_time, another_time):
                return None
        self._assert_days_and_weeks_same(one_time, another_time)

    @staticmethod
    def _is_weeks_and_days_same(one_time, another_time):
        return (one_time.day == another_time.day) and (one_time.week == another_time.week)

    @staticmethod
    def _are_day_and_week_nones(day, week):
        return (day is None) and (week is None)

    @staticmethod
    def _are_day_and_week_set(day, week):
        return (day is not None) and (week is not None)

    def _is_day_and_week_in_self_or_other_nones(self,
                                                one_time: "Time" or "TimeRange",
                                                another_time: "Time" or "TimeRange"):
        return (self._are_day_and_week_nones(one_time.day, one_time.week) or
                self._are_day_and_week_nones(another_time.day, another_time.week))

    def _assert_days_and_weeks_same(self, one_time, another_time):
        if self._is_weeks_and_days_same(one_time, another_time):
            raise RuntimeError("Operation forbidden for times with different days")

    def _assert_day_and_week_are_both_set_or_both_none(self, day, week):
        assert self._are_day_and_week_nones(day, week) or self._are_day_and_week_set(day, week)

    @staticmethod
    def _assert_day_and_week_types_correctness(day, week):
        assert (day in DAYS) or (day is None)
        assert (isinstance(week, Week)) or (Week is None)

