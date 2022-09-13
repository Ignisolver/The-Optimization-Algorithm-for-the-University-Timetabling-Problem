from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from time_.time_range.time_range_utils import TimeRangeIntersectDetector, TimeRangeInitializer
from utils.types_ import Day, Week, TimeRangeType
from time_.time_utils import DateCorrectnessCaretaker
from time_ import TimeDelta

if TYPE_CHECKING:
    from time_.time_ import Time


@dataclass
class TimeRange(TimeRangeType):
    start: Union["Time", None] = None
    end: Union["Time", None] = None
    dur: Union[TimeDelta, None] = None
    day: Union[Day, None] = None
    week: Union[Week, None] = None
    _intersect_detector = TimeRangeIntersectDetector()
    _date_correctness = DateCorrectnessCaretaker()
    _initializer = TimeRangeInitializer()

    def __post_init__(self):
        self._date_correctness.assert_initial_arguments_day_and_week_correct(self.day, self.week)
        self.start, self.dur, self.end = self._initializer.calc_start_dur_end(self.start, self.dur, self.end)

    def increase_end(self, time_delta: TimeDelta):
        self.end += time_delta
        self.dur += time_delta
        self._initializer.assert__start_dur_end__correct(self.start, self.end, self.dur)

    def decrease_start(self, time_delta: TimeDelta):
        self.start -= time_delta
        self.dur += time_delta
        self._initializer.assert__start_dur_end__correct(self.start, self.end, self.dur)

    def expand_start_and_end(self, time_delta: TimeDelta):
        self.increase_end(time_delta)
        self.decrease_start(time_delta)

    def intersect(self: "TimeRange", other: Union["Time", "TimeRange"]) -> bool:
        self._date_correctness.assert_days_and_weeks_correctness(self, other)
        return self._intersect_detector.is_intersection(self, other)
