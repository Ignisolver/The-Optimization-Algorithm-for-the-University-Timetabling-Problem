from typing import Tuple, TYPE_CHECKING
from time_.time_utils import DateCorrectnessCaretaker


if TYPE_CHECKING:
    from time_.time_range.time_range import TimeRange
    from time_.time_ import Time
    from time_.time_delta import TimeDelta


class TimeRangeIntersectDetector:
    def is_intersection(self,
                        one: "TimeRange",
                        other: "Time" or "TimeRange") -> bool:
        if isinstance(other, Time):
            return self._is_time_in_time_range(one, other)

        if isinstance(other, TimeRange):
            return self._is_time_ranges_intersect(one, other)

    @staticmethod
    def _one_is_in_other(one, other) -> bool:
        return other.start <= one.start and one.end <= other.end

    @staticmethod
    def _other_is_in_one(one, other) -> bool:
        return one.start <= other.start and other.end <= one.end

    @staticmethod
    def _other_ends_in_one(one, other) -> bool:
        return one.start < other.end <= one.end

    @staticmethod
    def _other_starts_in_one(one, other) -> bool:
        return one.start <= other.start < one.end

    @staticmethod
    def _is_time_in_time_range(one, time):
        return one.start < time < one.end

    def _is_time_ranges_intersect(self, tr_1, tr_2):
        if (self._other_starts_in_one(tr_1, tr_2) or
                self._other_ends_in_one(tr_1, tr_2) or
                self._other_is_in_one(tr_1, tr_2) or
                self._one_is_in_other(tr_1, tr_2)):
            return True
        else:
            return False


class TimeRangeInitializer:
    def __init__(self):
        self._init_start: "Time" or None = None
        self._init_end: "Time" or None = None
        self._init_end: "Time" or None = None
        self._date_correctness = DateCorrectnessCaretaker()

    @staticmethod
    def _assert_2_of__start_end_dur__not_none(time_range: "TimeRange"):
        nones_amount = sum(1 for x in (time_range.start, time_range.end, time_range.dur) if x is None)
        if nones_amount >= 2:
            raise ValueError("To less information to specify TimeRange")

    def _assert_arguments_correctness(self, time_range: "TimeRange"):
        self._date_correctness.assert_arguments_day_and_week_correct(time_range.day, time_range.week)
        self._assert_2_of__start_end_dur__not_none(time_range)

    @staticmethod
    def _assert__start_dur_end__correct(time_range: "TimeRange"):
        if time_range.end - time_range.start != time_range.dur:
            raise ValueError("Incorrect time range data passed")

    def _calc_start(self, time_range: "TimeRange"):
        self._init_start = time_range.end - time_range.dur
        self.assert_start_is_less_then_end(time_range.start, time_range.end)

    def _calc_end(self, time_range: "TimeRange"):
        self._init_end = time_range.start + time_range.dur
        self.assert_start_is_less_then_end(time_range.start, self._init_end)

    @staticmethod
    def _is_only_start_given(time_range: "TimeRange") -> bool:
        return (time_range.end is None) and (time_range.start is not None)

    @staticmethod
    def _is_only_end_given(time_range: "TimeRange") -> bool:
        return (time_range.end is not None) and (time_range.start is None)

    @staticmethod
    def _are_both_start_and_end_given(time_range: "TimeRange"):
        return (time_range.end is not None) and (time_range.start is not None)

    def _calc_start_or_end(self, time_range: "TimeRange"):
        if self._is_only_start_given(time_range):
            self._calc_end(time_range)
        elif self._is_only_end_given(time_range):
            self._calc_start(time_range)
        elif self._are_both_start_and_end_given(time_range):
            self._assert__start_dur_end__correct(time_range)

    def _calc_dur(self, time_range: "TimeRange"):
        self.assert_start_is_less_then_end(time_range.start, time_range.end)
        self._init_dur = time_range.end - time_range.start

    @staticmethod
    def assert_start_is_less_then_end(start, end):
        if end < start:
            raise RuntimeError("An attempt to shrink TimeRange for negative size")

    @staticmethod
    def _is_duration_given(time_range: "TimeRange"):
        return time_range.dur is not None

    def calc_start_dur_end(self, time_range: "TimeRange") -> Tuple["Time", "Time", "TimeDelta"]:
        if self._is_duration_given(time_range):
            self._calc_start_or_end(time_range)
        else:
            self._calc_dur(time_range)

        return self._init_start, self._init_dur, self._init_end
