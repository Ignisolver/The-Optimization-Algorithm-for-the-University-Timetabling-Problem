from typing import Iterator

from algorithm.best_times_finder import get_best_time
from algorithm.check_on_time import select_room
from basic_structures import Classes


def algorithm(classes_list: Iterator[Classes]):
    for classes in classes_list:
        rooms = classes.get_sorted_rooms()
        for start in get_best_time(classes):
            room = select_room(classes, rooms, start)
            if room is None:
                continue
            else:
                classes.assign(start.time, room, start.day)
        print("assign")



