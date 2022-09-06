from dataclasses import dataclass


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


class Time:
    def __init__(self, hour, minute):
        assert 0 <= hour <= 23
        assert 0 <= minute <= 59
        assert isinstance(hour, int)
        assert isinstance(minute, int)
        self.hour = hour
        self.minute = minute

    def __sub__(self, other: "Time" or TimeDelta) -> TimeDelta or "Time":
        if isinstance(other, Time):
            return TimeDelta(minutes=int(self) - int(other))
        elif isinstance(other, TimeDelta):
            minutes = self.minute - other.minutes
            hours = self.hour - other.hours + (minutes // 60)
            minutes = minutes % 60
            return Time(hours, minutes)

    def __add__(self, other: TimeDelta) -> "Time":
        minutes = self.minute + other.minutes
        hours = self.hour + other.hours + (minutes // 60)
        minutes = minutes % 60
        return Time(hours, minutes)

    def __repr__(self):
        return f"Time(hours: {self.hour}; minutes: {self.minute})"

    def __lt__(self, other):
        return int(self) < int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __eq__(self, other: "Time"):
        return int(self) == int(other)

    def __int__(self):
        return self.hour * 60 + self.minute


@dataclass
class TimeRange:
    start: Time = None
    dur: TimeDelta = None
    end: Time = None

    def __post_init__(self):
        if self.dur is not None:
            if self.end is None and self.start is not None:
                self.end = self.start + self.dur
            elif self.end is not None and self.start is None:
                self.start = self.end - self.dur
            elif self.end is not None and self.start is not None:
                if self.end - self.start != self.dur:
                    raise ValueError("Incorrect time range data passed")
            else:
                raise ValueError("To less information to specify TimeRange")

        if self.dur is None:
            if self.start is None or self.end is None:
                raise ValueError("To less information to specify TimeRange")
            else:
                self.dur = self.end - self.start
                if self.dur < 0:
                    raise ValueError("Start time is grater then end time")

    # todo przecinanie z Range lub Time
    # todo operacje arytmetyczne z Time / timedelta







