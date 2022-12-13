import os
from typing import Iterable, Type, TYPE_CHECKING

import sys

from data_generation.basic_config import MIN_HOUR, MAX_HOUR

if TYPE_CHECKING:
    from time_ import Time


def check_type_all(iterable: Iterable, type_: Type):
    return all(isinstance(element, type_) for element in iterable)


def check_if_time_is_available(times: Iterable["Time"]):
    if not all(map(lambda time: MIN_HOUR <= time <= MAX_HOUR, times)):
        raise ValueError("Time outside time limits")


def turn_off_print():
    sys.stdout = open(os.devnull, 'w')

