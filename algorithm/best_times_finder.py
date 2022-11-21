from dataclasses import dataclass
from random import shuffle
from typing import List, Iterator

from algorithm.goal_function import evaluate
from algorithm.merge_week_schedule import get_free_ranges_from_week_schedules
from basic_structures import Classes
from data_generation.generation_configs import TIME_GRANULATION
from time_ import TimeRange as TR, TimeDelta as TD, Time
from utils.types_ import Day


# testme all
# not sort but max

@dataclass
class Start:
    time: Time
    day: Day


def _get_start_times(ranges: List[TR], dur: TD) -> List[Start]:
    starts = []
    for tr in ranges:
        start = tr.start
        end = tr.end - dur
        while start <= end:
            starts.append(Start(start, tr.day))
            start += TIME_GRANULATION
    return starts


def _available_start_times(classes: Classes) -> Iterator[Start]:
    with_schedules = classes.get_with_schedules()
    ranges = get_free_ranges_from_week_schedules(with_schedules, classes.dur)
    start_times = _get_start_times(ranges, classes.dur)
    return iter(start_times)


def _evaluate_time(classes: Classes, start: Start):
    classes.temp_assign(start.time, start.day)
    schedules = classes.groups
    val = evaluate(schedules)
    classes.unassign_temp()
    return val


def get_best_time(classes: Classes) -> Iterator[Start]:
    times_values = []
    for start in _available_start_times(classes):
        val = _evaluate_time(classes, start)
        times_values.append((start, val))
    shuffle(times_values)
    while len(times_values) != 0:
        time_val = min(times_values, key=lambda td_v: td_v[1])
        yield time_val[0]
        times_values.remove(time_val)
