from dataclasses import dataclass

from time_ import Time
from utils.types_ import Day


@dataclass
class Availability:
    day: Day
    start: Time
    end: Time
    dur = None

    def __post_init__(self):
        self.dur = self.end - self.start
