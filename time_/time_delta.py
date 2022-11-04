from numba import uint8, int8, int32

spec = [
    ("hours", int8),
    ("minutes", int32),
    ("type", uint8)
]

hour_dict = tuple((i*60 for i in range(24)))


class TimeDelta:
    def __init__(self, hours=0, minutes=0):
        if minutes > 59:
            self.hours = hours + minutes // 60
            self.minutes = minutes % 60
        else:
            self.hours = hours
            self.minutes = minutes
        self.type = 1

    def __hash__(self):
        return hash((self.hours, self.minutes, self.type))

    def __neg__(self):
        return TimeDelta(-self.hours, -self.minutes)

    def __int__(self):
        return hour_dict[self.hours] + self.minutes

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
