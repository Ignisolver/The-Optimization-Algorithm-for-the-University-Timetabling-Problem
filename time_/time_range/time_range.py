from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from time_.time_range.time_range_utils import TimeRangeIntersectDetector, TimeRangeInitializer
from utils.types_ import Day, Week
from time_.time_utils import DateCorrectnessCaretaker
from time_ import TimeDelta

if TYPE_CHECKING:
    from time_.time_ import Time


class TimeRange:
    def __init__(self):
        self.start: Union["Time", None] = None
        self.end: Union["Time", None] = None
        self.dur: Union[TimeDelta, None] = None
        self.day: Union[Day, None] = None
        self.week: Union[Week, None] = None
        self._intersect_detector = TimeRangeIntersectDetector()
        self._date_correctness = DateCorrectnessCaretaker()
        self._initializer = TimeRangeInitializer()

    def __post_init__(self):
        self._date_correctness.assert_initial_arguments_day_and_week_correct(self.day, self.week)
        self.start, self.dur, self.end = self._initializer.get_filled_start_dur_end(self.start, self.dur, self.end)

    def change_end(self, time_delta: TimeDelta):
        self.end += time_delta
        self.dur += time_delta
        self._initializer.assert_start_is_less_then_end(self.start, self.end)

    def change_start(self, time_delta: TimeDelta):
        self.start -= time_delta
        self.dur += time_delta
        self._initializer.assert_start_is_less_then_end(self.start, self.end)

    def change_start_and_end(self, time_delta: TimeDelta):
        self.start = self.start - time_delta
        self.end = self.end + time_delta
        self.dur = self.dur + time_delta + time_delta
        self._initializer.assert_start_is_less_then_end(self.start, self.end)

    def __mul__(self: "TimeRange", other: Union["Time", "TimeRange"]) -> bool:
        self._date_correctness.assert_days_and_weeks_correctness(self, other)
        return self._intersect_detector.is_intersection(self, other)
