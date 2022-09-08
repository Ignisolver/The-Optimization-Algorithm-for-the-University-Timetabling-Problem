from dataclasses import dataclass
from typing import Iterable

from constans import DAYS
from types_ import Day, Week


# todo missing tests + day tests

class TimeDelta:
    def __init__(self, hours=0, minutes=0):
        assert isinstance(minutes, int)
        assert isinstance(hours, int)

        minutes = hours * 60 + minutes
        sign = 1 if minutes >= 0 else -1
        minutes = abs(minutes)

        self.hours = sign * minutes // 60
        self.minutes = sign * minutes % 60

    def __neg__(self):
        return TimeDelta(-self.hours, -self.minutes)

    def __int__(self):
        return self.hours * 60 + self.minutes

    def __repr__(self):
        return f"TimeDelta(hours: {self.hours}; minutes: {self.minutes})"

    def __add__(self, other: "TimeDelta"):
        minutes = self.minutes + other.minutes
        hours = self.hours + other.hours

        return TimeDelta(hours, minutes)

    def __sub__(self, other):
        minutes = self.minutes - other.minutes
        hours = self.hours - other.hours
        return TimeDelta(hours, minutes)

    def __eq__(self, other: "TimeDelta"):
        return self.hours == other.hours and self.minutes == other.minutes

    def __lt__(self, other):
        return int(self) < int(other)

    def __le__(self, other):
        return int(self) <= int(other)


class TimeCaretaker:
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

    def assert_day_and_week_correctness(self, one_time: "Time", another_time: "Time", none_able=False):
        if none_able:
            if self._is_day_and_week_in_self_or_other_nones(one_time, another_time):
                return None
        self._assert_days_and_weeks_same(one_time, another_time)

@dataclass
class Time:
    hour: int
    minute: int
    day: Day = None
    week: Week = None
    tim_car = TimeCaretaker()

    def __post_init__(self):
        assert 0 <= self.hour <= 23
        assert 0 <= self.minute <= 59
        assert (self.day in DAYS) or (self.day is None)
        assert (isinstance(self.week, Week)) or (self.day is None)



    def __sub__(self, other: "Time" or TimeDelta) -> TimeDelta or "Time":
        if isinstance(other, Time):
            self.tim_car.assert_day_and_week_correctness(self, other)
            return TimeDelta(minutes=int(self) - int(other))

        elif isinstance(other, TimeDelta):
            minutes = self.minute - other.minutes
            hours = self.hour - other.hours + (minutes // 60)
            minutes = minutes % 60
            return Time(hours, minutes, self.day, self.week)

    def __add__(self, other: TimeDelta) -> "Time":
        minutes = self.minute + other.minutes
        hours = self.hour + other.hours + (minutes // 60)
        minutes = minutes % 60
        return Time(hours, minutes, self.day, self.week)

    def __lt__(self, other: "Time"):
        self.tim_car.assert_day_and_week_correctness(self, other, none_able=True)
        return int(self) < int(other)

    def __le__(self, other: "Time"):
        self.tim_car.assert_day_and_week_correctness(self, other, none_able=True)
        return int(self) <= int(other)

    def __eq__(self, other: "Time"):
        self.tim_car.assert_day_and_week_correctness(self, other, none_able=True)
        return int(self) == int(other)

    def __int__(self):
        return self.hour * 60 + self.minute


@dataclass
class TimeRange:
    start: Time = None
    dur: TimeDelta = None
    end: Time = None
    day: Day = None
    week: Week = None

    def _assert_2_of__start_end_dur__present(self):
        nones_amount = sum(1 for x in (self.start, self.end, self.dur) if x is None)
        if nones_amount >= 2:
            raise ValueError("To less information to specify TimeRange")

    def _assert_arguments_corectness(self):
        assert self.day is not None
        assert self.week is not None
        self._assert_2_of__start_end_dur__present()

    def _assert_all_correct(self):
        if self.end - self.start != self.dur:
            raise ValueError("Incorrect time range data passed")

    def _calc_start(self):
        self.start = self.end - self.dur
        self._assert_start_is_less_then_end(self.start, self.end)

    def _calc_end(self):
        self.start = self.end - self.dur
        self._assert_start_is_less_then_end(self.start, self.end)

    def _calc_start_or_end(self):
        if self.end is None and self.start is not None:
            self._calc_end()
        elif self.end is not None and self.start is None:
            self._calc_start()
        elif self.end is not None and self.start is not None:
            self._assert_all_correct()

    def _calc_dur(self):
        self.dur = self.end - self.start
        self._assert_start_is_less_then_end(self.start, self.end)

    def __post_init__(self):
        if self.dur is not None:
            self._calc_start_or_end()

        if self.dur is None:
            self._calc_dur()

    @staticmethod
    def _is_all_nones(item: Iterable):
        return not any(item)

    def _is_day_and_week_same(self, other):
        return self.day != other.day or self.week != other.week

    def _assert_same_day_and_week(self, other: Time or "TimeRange"):
        if self._is_all_nones((self.day, other.day, self.week, other.week)):
            if self._is_day_and_week_same(other):
                raise RuntimeError("Operation forbidden for times with different days")

    def change_end(self, time_delta: TimeDelta):
        # todo test
        self.end += time_delta
        self.dur += time_delta
        self._assert_start_is_less_then_end(self.start, self.end)

    def change_start(self, time_delta: TimeDelta):
        # todo test
        self.start -= time_delta
        self.dur += time_delta
        self._assert_start_is_less_then_end(self.start, self.end)

    def change_start_and_end(self, time_delta: TimeDelta):
        # todo test
        self.start = self.start - time_delta
        self.end = self.end + time_delta

        self._assert_start_is_less_then_end(self.start, self.end)

        self.dur = self.dur + time_delta + time_delta

    @staticmethod
    def _assert_start_is_less_then_end(start, end):
        # todo test
        if end < start:
            raise RuntimeError("An attempt to shrink TimeRange for negative size")

    def _self_is_in_other(self, other) -> bool:
        # todo test
        return other.start <= self.start and self.end <= other.end

    def _other_is_in_self(self, other) -> bool:
        # todo test
        return self.start <= other.start and other.end <= self.end

    def _other_ends_in_self(self, other) -> bool:
        # todo test
        return self.start < other.end <= self.end

    def _other_starts_in_self(self, other) -> bool:
        # todo test
        return self.start <= other.start < self.end

    def _is_time_in_time_range(self, time):
        return self.start < time < self.end
    
    def _is_time_ranges_intersect(self, time_range):
        if (self._other_starts_in_self(time_range) or
                self._other_ends_in_self(time_range) or
                self._other_is_in_self(time_range) or
                self._self_is_in_other(time_range)):
            return True
        else:
            return False

    def __mul__(self: "TimeRange", other: Time or "TimeRange") -> bool:
        # todo test
        # Does two time ranges, or time and time range intersects
        self._assert_same_day_and_week(other)

        if isinstance(other, Time):
            return self._is_time_in_time_range(other)

        if isinstance(other, TimeRange):
            return self._is_time_ranges_intersect(other)