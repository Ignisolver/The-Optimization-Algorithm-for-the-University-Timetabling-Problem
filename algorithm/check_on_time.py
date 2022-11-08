from typing import List

from algorithm.best_times_finder import Start
from basic_structures import Classes, Room
from basic_structures.with_schedule import WithSchedule
from time_ import Time
from utils.distanses_manager import Distances
from utils.types_ import ClassesType


# testme all


def _is_being_on_time_is_certain(classes: Classes):
    if classes is None or classes.classes_type == ClassesType.UNAVAILABLE:
        return True


def _is_availability_to_be_on_time(end_time: Time,
                                   start_time: Time,
                                   r1: Room,
                                   r2: Room):
    buffer_time = start_time - end_time
    distance_time = Distances()[r1, r2]
    if distance_time > buffer_time:
        return False
    return True


def is_before_ok(item, day, start_time, room):
    cl_before = item.week_schedule.days[day].get_last_classes_before(
        start_time)
    if not _is_being_on_time_is_certain(cl_before):
        return _is_availability_to_be_on_time(cl_before.end_time,
                                              start_time, room, cl_before.room)
    return True


def is_after_ok(item, day, start_time, room, dur):
    cl_after = item.week_schedule.days[day].get_next_classes_after(start_time)
    if not _is_being_on_time_is_certain(cl_after):
        return _is_availability_to_be_on_time(start_time + dur,
                                              cl_after.start_time,
                                              room, cl_after.room)
    return True


def _check_room_not_too_far_for_schedule(item: WithSchedule, classes: Classes,
                                         room: Room, start: Start):
    avail_bef = is_before_ok(item, classes.day, start.time, room)
    avail_aft = is_after_ok(item, classes.day, start.time, room, classes.dur)
    return avail_aft and avail_bef


def _is_classes_room_not_to_far(classes: Classes,
                                room: Room,
                                start: Start):
    items = classes.groups
    for item in items:
        if not _check_room_not_too_far_for_schedule(item, classes, room, start):
            return False
    return True


def select_room(classes: Classes, rooms: List[Room], start: Start):
    for room in rooms:
        if room.is_assignment_available(start, classes):
            if _is_classes_room_not_to_far(classes, room, start):
                return room
    return None





