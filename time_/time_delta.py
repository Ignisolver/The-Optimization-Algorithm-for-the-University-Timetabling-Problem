class TimeDelta:
    def __init__(self, hours=0, minutes=0):
        assert isinstance(hours, int)
        assert isinstance(minutes, int)
        minutes = self._calc_total_amount_of_minutes(hours, minutes)
        self.hours = minutes // 60
        self.minutes = minutes % 60

    @staticmethod
    def _calc_total_amount_of_minutes(hours, minutes) -> int:
        minutes = hours * 60 + minutes
        sign = 1 if minutes >= 0 else -1
        minutes = abs(minutes)
        return sign * minutes

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
