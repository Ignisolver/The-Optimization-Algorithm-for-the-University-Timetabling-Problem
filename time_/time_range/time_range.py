from dataclasses import dataclass
from typing import TYPE_CHECKING, Union, List

from time_.time_range.time_range_utils import (TimeRangeIntersectDetector,
                                               TimeRangeInitializer)
from utils.types_ import Day, TimeRangeType
from time_ import TimeDelta

if TYPE_CHECKING:
    from time_.time_ import Time


@dataclass
class TimeRange(TimeRangeType):
    start: Union["Time", None] = None
    end: Union["Time", None] = None
    dur: Union[TimeDelta, None] = None
    day: Union[Day, None] = None
    _intersect_detector = TimeRangeIntersectDetector()
    _initializer = TimeRangeInitializer()

    def __post_init__(self):
        self.start, self.dur, self.end = self._initializer.\
            calc_start_dur_end(self.start, self.dur, self.end)

    def increase_end(self, time_delta: TimeDelta):
        self.end += time_delta
        self.dur += time_delta
        self._initializer.assert__start_dur_end__correct(self.start,
                                                         self.end,
                                                         self.dur)

    def decrease_start(self, time_delta: TimeDelta):
        self.start -= time_delta
        self.dur += time_delta
        self._initializer.assert__start_dur_end__correct(self.start,
                                                         self.end,
                                                         self.dur)

    def expand_start_and_end(self, time_delta: TimeDelta):
        self.increase_end(time_delta)
        self.decrease_start(time_delta)

    def intersect(self, other: Union["Time", "TimeRange"]) -> bool:
        if self.day != other.day:
            return False
        return self._intersect_detector.is_intersection(self, other)

    def to_generate(self) -> List:
        list_ = [self.day + 1,
                 [self.start.hour, self.start.minute],
                 [self.end.hour, self.end.minute]]
        return list_
