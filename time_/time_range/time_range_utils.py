from dataclasses import dataclass
from typing import TYPE_CHECKING, Union


from utils.none_machine import NM
from utils.singleton import SingletonMeta
from utils.types_ import TimeType, TimeRangeType

if TYPE_CHECKING:
    from time_.time_ import Time
    from time_.time_range import TimeRange
    from time_.time_delta import TimeDelta


class TimeRangeIntersectDetector(metaclass=SingletonMeta):
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


@dataclass
class StaDurEnd:
    start: "Time"
    dur: "TimeDelta"
    end: "Time"


class TimeRangeInitializer(metaclass=SingletonMeta):
    def calc_start_dur_end(self, sdn: StaDurEnd) -> StaDurEnd:
        # self._assert_2_of__start_end_dur__not_none(sdn.start, sdn.dur, sdn.end)
        if sdn.dur is None:
            sdn.dur = sdn.end - sdn.start
        elif sdn.start is None:
            sdn.start = sdn.end - sdn.dur
        elif sdn.end is None:
            sdn.end = sdn.start + sdn.dur

        # self.assert__start_dur_end__correct(sdn.start, sdn.end, sdn.dur)

        return sdn

    @staticmethod
    def _assert_2_of__start_end_dur__not_none(start, end, dur):
        nones_amount = NM.count_nones((start, end, dur))
        if nones_amount >= 2:
            raise ValueError("To less information to specify TimeRange")

    @staticmethod
    def assert__start_dur_end__correct(start, end, dur):
        if (end - start != dur) or (dur < 0):
            raise ValueError("Incorrect time range data passed")
