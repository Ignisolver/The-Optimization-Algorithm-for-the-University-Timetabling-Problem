# classes for groups
# rooms for classes
# lecturers for classes

import random
import string
from dataclasses import dataclass
from itertools import cycle
from random import randint
from typing import List

from basic_structures import Room, Group, Lecturer, Classes
from basic_structures.classes import UnavailableClasses
from basic_structures.room import Building
from data import MIN_HOUR, MAX_HOUR, TIME_GRANULATION
from data_generation.generation_configs import *
from time_ import TimeDelta, Time
from utils.constans import DAYS
from utils.distanses_manager import Distances
from utils.types_ import ClassesType as CT

random.seed(1)


@dataclass
class All:
    buildings: List[Building]
    rooms: List[Room]
    lecturers: List[Lecturer]
    classes: List[Classes]
    groups: List[Group]
    distances: Distances


def get_random_name():
    size = randint(4, 10)
    letters = [random.choice(string.ascii_lowercase) for _ in range(size)]
    name = "".join(letters)
    return name


def get_random_start_time(dur):
    max_t = MAX_HOUR - dur - TimeDelta(1)
    h = randint(MIN_HOUR.hour, max_t.hour)
    m = randint(0, 59) // TIME_GRANULATION * TIME_GRANULATION
    return Time(h, m)


def get_random_day():
    return random.choice(DAYS)


def names_generator():
    while True:
        yield get_random_name()


def id_generator():
    id_ = 0
    while True:
        yield id_
        id_ += 1


ig_rooms = id_generator()


def generate_buildings():
    buildings = [Building(i) for i in range(AMOUNT_OF_BUILDINGS)]
    return buildings


def generate_distances(buildings):
    distances = Distances()
    dbb = cycle(DISTANCES_BETWEEN_BUILDINGS)
    buld_amount = len(buildings)
    for i in range(buld_amount):
        b1 = buildings[i]
        for b2 in buildings[i:]:
            distances[b1, b2] = next(dbb)


def generate_rooms(buildings, amounts, capacities):
    ng = names_generator()
    cg = cycle(capacities)
    rag = cycle(amounts)
    init_aval = int((MAX_HOUR - MIN_HOUR)) * 5
    rooms = []
    for room_amount, building in zip(rag, buildings):
        for _ in range(room_amount):
            r = Room(id_=next(ig_rooms),
                     _initial_availability_minutes=init_aval,
                     people_capacity=next(cg), name=next(ng),
                     build_id=building.id_)
            building.rooms.append(r)
            rooms.append(r)
    return rooms


def _try_to_assign_unavaileble_classes(id_, obj, dur):
    for i in range(10):
        day = get_random_day()
        start_time = get_random_start_time(dur)
        try:
            unav_cl = UnavailableClasses(id_=id_, start=start_time,
                                         day=day, dur=dur)
            obj.assign(unav_cl)
            break
        except Exception as e:
            print(e)
            continue
    else:
        raise RuntimeError("Can not assign unavailable to room")


def generate_groups():
    groups = []
    ig = id_generator()
    ng = names_generator()
    students_amount = cycle(AMOUNT_OF_STUDENTS_PER_GROUP)
    n_groups_in_field = cycle(AMOUNT_OF_GROUPS_IN_FIELD)
    n_groups = sum(next(n_groups_in_field) for _ in range(AMOUNT_OF_FIELDS))
    for _ in range(n_groups):
        group = Group(next(ig), next(ng), next(students_amount))
        groups.append(group)
    random.shuffle(groups)
    return groups


def generate_lecturers():
    lecturers = []
    ig = id_generator()
    ng = names_generator()
    for _ in range(AMOUNT_OF_LECTURERS):
        lecturer = Lecturer(next(ig), next(ng))
        lecturers.append(lecturer)
    return lecturers


def assign_unavailability(objects, amounts, durations):
    amounts_of_unav = cycle(amounts)
    random.shuffle(durations)
    ig = id_generator()
    durations = cycle(durations)
    for obj, unav_amount in zip(objects, amounts_of_unav):
        for len_ in range(unav_amount):
            dur = TimeDelta(0, next(durations))
            _try_to_assign_unavaileble_classes(next(ig), obj, dur)


def get_availeble_rooms(rooms, n):
    return random.sample(rooms, n)


def generate_classes(lecturers, lab_rooms, lect_rooms, groups):
    ids = id_generator()
    names = names_generator()
    lecturers_gen = cycle(lecturers)
    available_rooms_amounts = cycle(AVAILABLE_ROOMS_AMOUNT)
    subjects_amount = cycle(SUBJECTS_PER_FIELD)
    groups_amount = cycle(AMOUNT_OF_GROUPS_IN_FIELD)
    random.shuffle(DURATIONS_OF_CLASSES)
    durations = cycle(DURATIONS_OF_CLASSES)
    groups_gen = iter(groups)
    max_people_in_group = max(AMOUNT_OF_STUDENTS_PER_GROUP)
    classes = []

    for _ in range(AMOUNT_OF_FIELDS):
        n_groups = next(groups_amount)
        field_groups = tuple(g for _, g in zip(range(n_groups), groups_gen))
        n_subjects = next(subjects_amount)
        for _ in range(n_subjects):
            n_people = sum([g.amount_of_students for g in field_groups])
            lect_avail_rooms = tuple(
                filter(lambda r: r.people_capacity >= n_people, lect_rooms))
            avail_rooms = random.sample(lect_avail_rooms,
                                        min(len(lect_avail_rooms),
                                            next(available_rooms_amounts)))
            lecture = Classes(next(ids), next(names), next(durations),
                              CT.LECTURE, avail_rooms,
                              next(lecturers_gen), field_groups)
            classes.append(lecture)
            for group in field_groups:
                avail_lab_rooms = tuple(filter(lambda r: (
                            r.people_capacity <= max_people_in_group and r.people_capacity >= group.amount_of_students),
                                               lab_rooms))
                avail_rooms = random.sample(avail_lab_rooms,
                                            min(len(avail_lab_rooms),
                                                next(available_rooms_amounts)))
                lab = Classes(next(ids), next(names), next(durations),
                              CT.LABORATORY, avail_rooms,
                              next(lecturers_gen), (group,))
                classes.append(lab)
    return classes


def generate_all() -> All:
    buildings = generate_buildings()
    generate_distances(buildings)
    lab_rooms = generate_rooms(buildings, AMOUNT_OF_LAB_ROOMS,
                               LAB_ROOMS_CAPACITIES)
    lect_rooms = generate_rooms(buildings, AMOUNT_OF_LECT_ROOMS,
                                LECTURE_ROOM_CAPACITIES)
    groups = generate_groups()
    lecturers = generate_lecturers()
    assign_unavailability(lecturers,
                          AMOUNT_OF_RANDOM_UNAVAILABILITY_FOR_LECTURERS,
                          UNAVAILABILITY_DURATION_LECTURERS)
    assign_unavailability(lab_rooms + lect_rooms,
                          AMOUNT_OF_RANDOM_UNAVAILABILITY_FOR_ROOMS,
                          UNAVAILABILITY_DURATION_ROOMS)
    classes = generate_classes(lecturers, lab_rooms, lect_rooms, groups)
    rooms = lab_rooms + lect_rooms
    print("WYGENEROWANO:")
    print(f"Budynki: {len(buildings)}")
    print(f"Sale: {len(lab_rooms + lect_rooms)}")
    print(f"Grupy: {len(groups)}")
    print(f"Prowadzący: {len(lecturers)}")
    lect_am = len([cl for cl in classes if cl.classes_type == CT.LECTURE])
    print(f"Wykłady: {lect_am}")
    lab_am = len([cl for cl in classes if cl.classes_type == CT.LABORATORY])
    print(f"Ćwiczenia: {lab_am}")
    print(30 * '_')
    return All(buildings, rooms, lecturers, classes, groups, Distances())
