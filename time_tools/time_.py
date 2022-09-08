from dataclasses import dataclass

from time_tools.time_delta import TimeDelta
from time_tools.utils import DateCorrectnessCaretaker
from types_ import Day, Week


# todo tests, file split


@dataclass
class Time:
    hour: int
    minute: int
    day: Day = None
    week: Week = None
    _date_correctness = DateCorrectnessCaretaker()

    def __post_init__(self):
        assert 0 <= self.hour <= 23
        assert 0 <= self.minute <= 59
        self._date_correctness.assert_arguments_day_and_week_correct(self.day, self.week)

    def __sub__(self, other: "Time" or TimeDelta) -> TimeDelta or "Time":
        if isinstance(other, Time):
            self._date_correctness.assert_days_and_weeks_correctness(self, other)
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
        self._date_correctness.assert_days_and_weeks_correctness(self, other, none_able=True)
        return int(self) < int(other)

    def __le__(self, other: "Time"):
        self._date_correctness.assert_days_and_weeks_correctness(self, other, none_able=True)
        return int(self) <= int(other)

    def __eq__(self, other: "Time"):
        self._date_correctness.assert_days_and_weeks_correctness(self, other, none_able=True)
        return int(self) == int(other)

    def __int__(self):
        return self.hour * 60 + self.minute

