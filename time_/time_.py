from dataclasses import dataclass
from typing import Union

from time_ import TimeDelta
from utils.types_ import Day, TimeType

TorTD = Union["Time", "TimeDelta"]


@dataclass
class Time(TimeType):
    hour: int
    minute: int
    day: Union[Day, None] = None

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
        if isinstance(other, Time):
            self._assert_days_same(other)
            return TimeDelta(minutes=int(self) - int(other))

        if isinstance(other, TimeDelta):
            minutes = self.minute - other.minutes
            hours = self.hour - other.hours + (minutes // 60)
            minutes = minutes % 60
            return Time(hours, minutes, self.day)

    def __add__(self, other: TimeDelta) -> "Time":
        minutes = self.minute + other.minutes
        hours = self.hour + other.hours + (minutes // 60)
        minutes = minutes % 60
        return Time(hours, minutes, self.day)

    def __lt__(self, other: "Time"):
        self._assert_days_same(other)
        return int(self) < int(other)

    def __le__(self, other: "Time"):
        self._assert_days_same(other)

        return int(self) <= int(other)

    def __eq__(self, other: "Time"):
        self._assert_days_same(other)
        return int(self) == int(other)

    def __int__(self):
        return self.hour * 60 + self.minute

    def __repr__(self):
        return str(self.hour) + ':' + str(self.minute)


