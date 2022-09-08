from typing import TYPE_CHECKING

from constans import DAYS
from types_ import Week

if TYPE_CHECKING:
    from time_tools.time_ import Time
    from time_tools.time_range.time_range_ import TimeRange


class DateCorrectnessCaretaker:
    @staticmethod
    def _is_weeks_and_days_same(one_time, another_time):
        return (one_time.day != another_time.day) or (one_time.week != another_time.week)

    @staticmethod
    def _is_day_and_week_in_self_or_other_nones(one_time, another_time):
        return ((one_time.day is None) and (one_time.week is None) or
                (another_time.day is None) and (another_time.week is None))

    def _assert_days_and_weeks_same(self, one_time, another_time):
        if self._is_weeks_and_days_same(one_time, another_time):
            raise RuntimeError("Operation forbidden for times with different days")

    def assert_days_and_weeks_correctness(self, one_time: "Time" or "TimeRange",
                                          another_time: "Time" or "TimeRange",
                                          none_able=False):
        if none_able:
            if self._is_day_and_week_in_self_or_other_nones(one_time, another_time):
                return None
        self._assert_days_and_weeks_same(one_time, another_time)

    @staticmethod
    def assert_arguments_day_and_week_correct(day, week):
        assert (day in DAYS) or (day is None)
        assert (isinstance(week, Week)) or (day is None)
