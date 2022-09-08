from typing import Iterable, Type

from time_.time_ import Time

MIN_HOUR = Time(8,0)
MAX_HOUR = Time(20,0)


def check_type_all(iterable: Iterable, type_: Type):
    return all(isinstance(element, type_) for element in iterable)


def check_if_time_is_available(times: Iterable[Time]):
    if not all(map(lambda time: MIN_HOUR <= time <= MAX_HOUR, times)):
        raise ValueError("Time outside time limits")
