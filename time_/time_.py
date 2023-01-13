from dataclasses import dataclass
from typing import Union

from time_ import TimeDelta
from utils.types_ import Day, TimeType

TorTD = Union["Time", "TimeDelta"]


hour_dict = tuple((i*60 for i in range(24)))


@dataclass
class Time(TimeType):
    hour: int
    minute: int
    day: Union[Day, None] = None
    type = 0

    def __hash__(self):
        return hash((self.hour, self.minute, self.type))

    def _assert_hour_and_minute_correctness(self):
        assert 0 <= self.hour <= 23, f"Hour :{self.hour} is not in [0 - 23]"
        assert 0 <= self.minute <= 59, f"Minute :{self.minute} is not in [0 - 59]"

    def __post_init__(self):
        self._assert_hour_and_minute_correctness()

    def _assert_days_same(self, other):
        if (self.day is None) or (other.day is None):
            return None
        assert self.day == other.day

    def __sub__(self, other: TorTD) -> TorTD:
        if other.type == 0:
            hours = self.hour - other.hour
            minutes = self.minute - other.minute
            return TimeDelta(hours, minutes)

        if other.type == 1:
            h_minus = 0
            if self.minute >= other.minutes:
                minutes = self.minute-other.minutes
            else:
                minutes = self.minute + 60 - other.minutes
                h_minus = 1
            hours = self.hour - other.hours - h_minus
            return Time(hours, minutes, self.day)

    def __add__(self, other: TimeDelta) -> "Time":
        minutes = self.minute + other.minutes
        if minutes > 59:
            hours = self.hour + other.hours + 1
            minutes = minutes - 60
        else:
            hours = self.hour + other.hours
        return Time(hours, minutes, self.day)

    def __lt__(self, other: "Time"):
        # self._assert_days_same(other)
        if self.hour < other.hour:
            return True
        if self.hour == other.hour:
            if self.minute < other.minute:
                return True
        return False

    def __le__(self, other: "Time"):
        # self._assert_days_same(other)
        if self.hour < other.hour:
            return True
        if self.hour == other.hour:
            if self.minute <= other.minute:
                return True
        return False

    def __eq__(self, other: "Time"):
        # self._assert_days_same(other)
        return self.hour == other.hour and self.minute == other.minute

    def __int__(self):
        return hour_dict[self.hour] + self.minute

    def __repr__(self):
        txt = f'{self.hour}:{self.minute:>02}'
        return txt