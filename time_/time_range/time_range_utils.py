from typing import Tuple, TYPE_CHECKING, Union

#  todo give as litte information as needed, @staticmethods

if TYPE_CHECKING:
    from time_.time_range import TimeRange
    from time_.time_ import Time
    from time_.time_delta import TimeDelta


class TimeRangeIntersectDetector:
    def is_intersection(self,
                        one: "TimeRange",
                        other: Union["Time", "TimeRange"]) -> bool:
        if isinstance(other, Time):
            return self._is_time_in_(one, other)

        if isinstance(other, TimeRange):
            return self._is_s_intersect(one, other)

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
    def _is_time_in_(one, time):
        return one.start < time < one.end

    def _is_s_intersect(self, tr_1, tr_2):
        if (self._other_starts_in_one(tr_1, tr_2) or
                self._other_ends_in_one(tr_1, tr_2) or
                self._other_is_in_one(tr_1, tr_2) or
                self._one_is_in_other(tr_1, tr_2)):
            return True
        else:
            return False


class TimeRangeInitializer:
    def __init__(self):
        self._init_start: "Time" = None
        self._init_dur: "Time" = None
        self._init_end: "Time" = None

        self._given_start: Union["Time", None] = None
        self._given_dur: Union["TimeDelta", None] = None
        self._given_end: Union["Time", None] = None

    def get_filled_start_dur_end(self, start, dur, end) -> Tuple["Time", "TimeDelta", "Time"]:
        self._assert_2_of__start_end_dur__not_none(start, dur, end)
        if dur is None:
            self._calc_dur(start, end)
        else:
            self._calc_start_or_end(start, dur, end)

        return self._init_start, self._init_dur, self._init_end

    @staticmethod
    def assert_start_is_less_then_end(start, end):
        if end <= start:
            raise RuntimeError("An attempt to shrink TimeRange for negative size")

    def _calc_start_or_end(start, dur, end):
        if self._is_only_start_given(start, dur, end):
            self._calc_end(start, dur)
        elif self._is_only_end_given(start, dur, end):
            self._calc_start(dur, end)
        elif self._are_both_start_and_end_given(start, end):
            self._assert__start_dur_end__correct()

    def _calc_dur(self):
        self.assert_start_is_less_then_end(self._given_start, self._given_end)
        self._init_dur = self._given_end - self._given_start

    def _calc_start(self):
        self._init_start = self._given_end - self._given_dur
        self.assert_start_is_less_then_end(self._init_start, self._given_end)

    def _calc_end(self):
        self._init_end = self._given_start + self._given_dur
        self.assert_start_is_less_then_end(self._given_start, self._init_end)

    def _assert_2_of__start_end_dur__not_none(self):
        nones_amount = sum(1 for x in (self._given_start, self._given_end, self._given_dur) if x is None)
        if nones_amount >= 2:
            raise ValueError("To less information to specify TimeRange")

    def _assert__start_dur_end__correct(self):
        if self._given_end - self._given_start != self._given_dur:
            raise ValueError("Incorrect time range data passed")

    def _is_only_start_given(self) -> bool:
        return (self._given_end is None) and (self._given_start is not None)

    def _is_only_end_given(self) -> bool:
        return (self._given_end is not None) and (self._given_start is None)

    def _are_both_start_and_end_given(self):
        return (self._given_end is not None) and (self._given_start is not None)

    def _is_duration_given(self, dur):
        return dur is not None



