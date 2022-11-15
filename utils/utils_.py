from typing import Iterable, Type, TYPE_CHECKING

from data_generation.generation_configs import MIN_HOUR, MAX_HOUR

if TYPE_CHECKING:
    from time_ import Time


def check_type_all(iterable: Iterable, type_: Type):
    return all(isinstance(element, type_) for element in iterable)


def check_if_time_is_available(times: Iterable["Time"]):
    if not all(map(lambda time: MIN_HOUR <= time <= MAX_HOUR, times)):
        raise ValueError("Time outside time limits")