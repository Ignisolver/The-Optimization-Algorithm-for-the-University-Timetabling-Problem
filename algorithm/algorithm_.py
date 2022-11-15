from dataclasses import dataclass
from typing import Iterator

from algorithm.best_times_finder import get_best_time
from algorithm.check_on_time import select_room
from basic_structures import Classes
from data_presentation.bar import bar


@dataclass
class AlgResult:
    successes: int = 0
    failures: int = 0
    failures_time: int = 0
    successes_time: int = 0


def algorithm(classes_list: Iterator[Classes]):
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
            # print(classes.id_, classes.groups, classes.lecturer, classes.avail_rooms)
            result.failures += 1
            result.failures_time += int(classes.dur)
    print(result)


