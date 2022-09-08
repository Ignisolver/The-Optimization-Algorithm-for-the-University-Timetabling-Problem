from dataclasses import dataclass

from time_tools.time_ import Time
from time_tools.time_range.utils import TimeRangeIntersectDetector, TimeRangeInitializer
from time_tools.time_delta import TimeDelta
from time_tools.utils import DateCorrectnessCaretaker
from types_ import Day, Week


@dataclass
class TimeRange:
    start: Time = None
    dur: TimeDelta = None
    end: Time = None
    day: Day = None
    week: Week = None
    _intersect_detector = TimeRangeIntersectDetector()
    _date_correctness = DateCorrectnessCaretaker()
    _initializer = TimeRangeInitializer()

    def __post_init__(self):
        self.start, self.dur, self.end = self._initializer.calc_start_dur_end(self)

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

    def __mul__(self: "TimeRange", other: Time or "TimeRange") -> bool:
        self._date_correctness.assert_days_and_weeks_correctness(self, other)
        return self._intersect_detector.is_intersection(self, other)
