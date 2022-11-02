# todo sort by am_of_people

from itertools import chain
from typing import List, Iterator, Callable

from basic_structures import Classes


def assign_occupacity(classes: List[Classes]):
    for cl in classes:
        cl.assign_occupacity()


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
    lol = []
    for classes in classes_nested:
        separated_list = _get_sorted_list(classes, key)
        lol.extend(separated_list)
    return lol


def _calc_am_of_people(classes: Classes):
    return sum([gr.amount_of_students for gr in classes.groups])


def sort_classes(classes: List[Classes]) -> Iterator[Classes]:
    sorted_1 = _split_classes([classes], lambda cl: len(cl.groups))
    sorted_2 = _split_classes(sorted_1, lambda cl: len(cl.avail_rooms))
    sorted_3 = _split_classes(sorted_2, lambda cl: cl.dur)
    sorted_4 = _split_classes(sorted_3, lambda cl: _calc_am_of_people(cl))
    return chain(*reversed(sorted_4))



