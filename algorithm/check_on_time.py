from typing import List

from algorithm.best_times_finder import Start
from basic_structures import Classes, Room
from basic_structures.with_schedule import WithSchedule
from time_ import TimeDelta
from utils.distanses_manager import Distances
from utils.types_ import ClassesType
# testme all


def _is_being_on_time_is_certain(classes: Classes):
    if classes is None or classes.classes_type == ClassesType.UNAVAILABLE:
        return True


def _is_availability_to_be_on_time(first_cl: Classes,
                                   sec_cl: Classes,
                                   classes: Classes,
                                   room: Room):
    r1 = first_cl.room if classes == sec_cl else sec_cl.room
    if not _is_being_on_time_is_certain(classes):
        buffer_time = sec_cl.start_time - first_cl.end_time
        distance_time = Distances()[r1, room]
        if distance_time > buffer_time:
            return False
    return True


def _check_room_not_too_far_for_schedule(item: WithSchedule,
                                       classes: Classes, room: Room):
    start_time = classes.start_time
    day = classes.day
    cl_before = item.week_schedule.days[day].get_last_classes_before(start_time)
    cl_after = item.week_schedule.days[day].get_next_classes_after(start_time)
    avail_bef = _is_availability_to_be_on_time(cl_before, classes,
                                               cl_before, room)
    avail_aft = _is_availability_to_be_on_time(classes, cl_after,
                                               cl_after, room)
    return avail_aft and avail_bef


def _is_classes_room_not_to_far(classes: Classes,
                                room: Room):
    items = classes.groups
    for item in items:
        if not _check_room_not_too_far_for_schedule(item, classes, room):
            return False
    return True


def select_room(classes: Classes, rooms: List[Room], start: Start):
    for room in rooms:
        if room.is_assignment_available(start, classes):
            if _is_classes_room_not_to_far(classes, room):
                return room
    return None





