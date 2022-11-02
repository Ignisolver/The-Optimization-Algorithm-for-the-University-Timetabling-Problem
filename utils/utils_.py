from typing import Iterable, Type, List, TYPE_CHECKING

from data import MIN_HOUR, MAX_HOUR

if TYPE_CHECKING:
    from time_ import TimeDelta as TD, Time, TimeRange as TR


def check_type_all(iterable: Iterable, type_: Type):
    return all(isinstance(element, type_) for element in iterable)


def check_if_time_is_available(times: Iterable["Time"]):
    if not all(map(lambda time: MIN_HOUR <= time <= MAX_HOUR, times)):
        raise ValueError("Time outside time limits")


def filter_times_grater_or_equal_than(times: List["TR"], time_delta: "TD"):
    return tuple(filter(lambda time: time.dur >= time_delta, times))
