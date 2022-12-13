import time
from typing import Iterator

from algorithm.alg_result import AlgResult
from algorithm.best_times_finder import get_best_time
from algorithm.check_on_time import select_room
from algorithm.time_measurement import measure_time
from basic_structures import Classes
from data_presentation.bar import bar


@measure_time
def algorithm(classes_list: Iterator[Classes]):
    print("ALGORITHM:")
    result = AlgResult()
    for classes in bar(classes_list, "ALGORITHM"):
        rooms = classes.get_sorted_rooms()
        for start in get_best_time(classes):
            room = select_room(classes, rooms, start)
            if room is None:
                continue
            else:
                classes.assign(start.time, room, start.day)
                result.successes += 1
                result.successes_time += int(classes.dur)
                break
        else:
            result.failures += 1
            result.failures_time += int(classes.dur)
    return result



