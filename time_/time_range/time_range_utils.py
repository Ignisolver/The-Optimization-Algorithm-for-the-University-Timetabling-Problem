from typing import Tuple, TYPE_CHECKING, Union

from utils.none_machine import NM
from utils.types_ import TimeType, TimeRangeType

if TYPE_CHECKING:
    from time_.time_ import Time
    from time_.time_range import TimeRange
    from time_.time_delta import TimeDelta


class TimeRangeIntersectDetector:
    def is_intersection(self,
                        one: "TimeRange",
                        other: Union["Time", "TimeRange"]) -> bool:
        if isinstance(other, TimeType):
            return self._is_time_in_time_range(time=other, one=one)

        if isinstance(other, TimeRangeType):
            return self._is_time_ranges_intersect(one, other)

    @staticmethod
    def _one_is_in_other(one, other) -> bool:
        return (other.start <= one.start) and (one.end <= other.end)

    @staticmethod
    def _other_is_in_one(one: "TimeRange", other: "TimeRange") -> bool:
        return (one.start <= other.start) and (other.end <= one.end)

    @staticmethod
    def _other_ends_in_one(one: "TimeRange", other: "TimeRange") -> bool:
        return one.start < other.end <= one.end

    @staticmethod
    def _other_starts_in_one(one: "TimeRange", other: "TimeRange") -> bool:
        return one.start <= other.start < one.end

    @staticmethod
    def _is_time_in_time_range(one: "TimeRange", time: "Time"):
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
    def calc_start_dur_end(self,
                           start=None,
                           dur=None,
                           end=None) -> Tuple["Time", "TimeDelta", "Time"]:
        self._assert_2_of__start_end_dur__not_none(start, dur, end)
        if dur is None:
            dur = self._calc_dur(start, end)
        elif start is None:
            start = self._calc_start(end, dur)
        elif end is None:
            end = self._calc_end(start, dur)

        self.assert__start_dur_end__correct(start, end, dur)

        return start, dur, end

    @staticmethod
    def _calc_dur(start, end):
        return end - start

    @staticmethod
    def _calc_start(end, dur):
        return end - dur

    @staticmethod
    def _calc_end(start, dur):
        return start + dur

    @staticmethod
    def _assert_2_of__start_end_dur__not_none(start, end, dur):
        nones_amount = NM.count_nones((start, end, dur))
        if nones_amount >= 2:
            raise ValueError("To less information to specify TimeRange")

    @staticmethod
    def assert__start_dur_end__correct(start, end, dur):
        if (end - start != dur) or (dur < 0):
            raise ValueError("Incorrect time range data passed")
