from typing import Iterator
from time import sleep
from algorithm.best_times_finder import get_best_time
from algorithm.check_on_time import select_room
from basic_structures import Classes
from data_presentation.bar import bar


def algorithm(classes_list: Iterator[Classes]):
    feilure_counter = 0
    for classes in bar(classes_list, "ALGORITHM"):
        rooms = classes.get_sorted_rooms()
        for start in get_best_time(classes):
            room = select_room(classes, rooms, start)
            if room is None:
                continue
            else:
                classes.assign(start.time, room, start.day)
                break
        else:
            feilure_counter += 1
    print("FAILURES:", feilure_counter)


