from dataclasses import dataclass
from typing import TYPE_CHECKING, Union, List

from time_ import TimeDelta
from time_.time_range.time_range_utils import (TimeRangeIntersectDetector as TRID,
                                               TimeRangeInitializer, StaDurEnd)
from utils.types_ import Day, TimeRangeType

if TYPE_CHECKING:
    from time_.time_ import Time

TRI = TimeRangeInitializer()


class TimeRange(TimeRangeType):
    def __init__(self, start=None, end=None, day=None):
        # sdn = StaDurEnd(start, dur, end)
        # sdn = TRI.calc_start_dur_end(sdn)
        self.day = day
        self.start = start
        self.end = end
        self.dur = end-start

    def intersect(self, other: Union["Time", "TimeRange"]) -> bool:
        if self.day != other.day:
            return False
        return TRID().is_intersection(self, other)

    def to_generate(self) -> List:
        list_ = [self.day + 1,
                 [self.start.hour, self.start.minute],
                 [self.end.hour, self.end.minute]]
        return list_
