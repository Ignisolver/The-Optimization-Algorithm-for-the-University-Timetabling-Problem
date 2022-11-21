from itertools import chain
from typing import List, Iterator, Callable

from basic_structures import Classes, Room
from data_generation.generator import All


def preprocess_all(all_: All):
    # assign_occupacity(all_.classes)  arleady done in gneration
    # add_info_to_week_schedule(all_.classes)  arleady done in gneration
    add_room_info(all_.rooms)
    sorted_classes = get_sorted_classes(all_.classes)
    calc_over_time_avail_time(all_)
    return sorted_classes


def assign_occupacity(classes: List[Classes]):
    for cl in classes:
        cl.assign_occupacity()


def add_room_info(rooms: List[Room]):
    for r in rooms:
        r.sum_occup_probab()


def add_info_to_week_schedule(classes: List[Classes]):
    for cl in classes:
        cl.add_info_to_week_schedule()


def calc_over_time_avail_time(all_: All):
    for item in (*all_.rooms, *all_.lecturers, *all_.groups):
        item.week_schedule.calc_over_time_avail_time()


def _create_container(classes, key) -> List:
    max_am_item = max(classes, key=key)
    max_amount = key(max_am_item)
    container = [[] for _ in range(max_amount + 1)]
    return container


def _remove_empty(classes_list: List[List[Classes]]) -> List[List[Classes]]:
    return [el for el in classes_list if el != []]


def _get_sorted_list(classes: List[Classes], key) -> List[List[Classes]]:
    separated_list = _create_container(classes, key)
    _sort_classes_list(classes, key, separated_list)
    separated_list = _remove_empty(separated_list)
    return separated_list


def _sort_classes_list(classes, key, separated_list):
    for cl in classes:
        val = key(cl)
        separated_list[val].append(cl)


def _split_classes(classes_nested: List[List[Classes]],
                  key: Callable[[Classes], int]) -> List[List[Classes]]:
    splited_list = []
    for classes in classes_nested:
        separated_list = _get_sorted_list(classes, key)
        splited_list.extend(separated_list)
    return splited_list


def _calc_am_of_people(classes: Classes):
    return sum([gr.amount_of_students for gr in classes.groups])


def get_sorted_classes(classes: List[Classes]) -> Iterator[Classes]:
    sorted_1 = _split_classes([classes], lambda cl: len(cl.groups))
    sorted_2 = _split_classes(sorted_1, lambda cl: len(cl.avail_rooms))
    del sorted_1
    sorted_3 = _split_classes(sorted_2, lambda cl: int(cl.dur))
    del sorted_2
    sorted_4 = _split_classes(sorted_3, lambda cl: _calc_am_of_people(cl))
    return list(chain(*reversed(sorted_4)))




