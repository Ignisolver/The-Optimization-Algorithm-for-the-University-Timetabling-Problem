from dataclasses import dataclass
from math import floor
from typing import List

from algorithm.goal_function import Metric, GFV
from basic_structures import Group
from basic_structures.with_schedule import WithSchedule
from data_generation.basic_config import MAX_TIME_PER_DAY
from data_generation.generator import All


@dataclass
class Result:
    all_vs_available: float
    # assigned_vs_available: str
    def __repr__(self):
        return str(round(self.all_vs_available, 1)) + "% of time remains available"


@dataclass
class Results:
    groups_res: Result
    lecturers_res: Result
    rooms_res: Result

    def __repr__(self):
        return (20 * "-" +
                "GROUPS    : " + str(self.groups_res) + "\n" +
                "LECTURERS : " + str(self.lecturers_res) + "\n" +
                "ROOMS     : " + str(self.rooms_res))


def summarize_before(all_: All):
    res = {}
    all_items = (all_.groups, all_.lecturers)
    names = ("GROUPS    :", "LECTURERS :")
    for name, items in zip(names, all_items):
        r = summarize_one(name, items)
        res.update(r)
    r = summarize_one("ROOMS     :", all_.rooms, room=True)
    res.update(r)
    print(30*'-')
    return res


def summarize_one(name, items, room=False):
    over_doable_hours = calc_over_doability_time(items, room=room)
    aval_time = calc_av_time_before(items, room=room)
    return represent_before(name, over_doable_hours, aval_time)


def summarize_after(all_: All, alg_res):
    print(alg_res)
    gfv_el, val = calc_goal_function_val(all_.groups)
    print(gfv_el, end='')
    print(30*"-")
    print(f"MEDIUM GOAL FUNCTION VALUE: {round(val,2)}")
    classes_time = sum(int(classes.dur) for classes in all_.classes if classes.start_time is not None)
    all_items = (all_.lecturers, all_.rooms)
    names = ("LECTURERS :", "ROOMS     :",)
    print(30 * "-")
    res = {}
    for name, items in zip(names, all_items):
        available_time = calc_av_time(items)
        r = represent_after(classes_time, available_time, name)
        res.update(r)
    return res, val, gfv_el


def calc_av_time(items: List[WithSchedule]):
    return sum(it.week_schedule.available_time for it in items)


def calc_av_time_before(items: List[WithSchedule], room=False):
    for item in items:
        item.week_schedule.calc_over_time_avail_time(room=room)
    all_free_time = sum(it.week_schedule.available_time for it in items)/60
    return all_free_time


def calc_over_doability_time(items: List[WithSchedule], room=False):
    for item in items:
        item.week_schedule.calc_over_time_avail_time(room=room)
    return floor(sum(it.week_schedule.over_doable for it in items) / 60)


def represent_after(classes_time, available_time, name):
    occupied_time = round(classes_time / available_time * 100, 1)
    print(name,
          f"{occupied_time:4>} % time occupied")
    return {name: occupied_time}


def represent_before(name, over_doable_hours, max_time):
    usage = round((1 + over_doable_hours/max_time) * 100, 1)
    if over_doable_hours >= 0:
        print(name,
              f"RESOURCE USAGE: {usage} | ",
              f"{over_doable_hours} hours unassignable")
    else:
        print(name,
              f"RESOURCE USAGE: {usage} % | ",
              f"{-over_doable_hours} hours available beyond necessary")
    return {name:usage}


def calc_goal_function_val(groups: List[Group]):
    val_el = GFV(0, 0, 0, 0)
    val = 0
    for gr in groups:
        m = Metric(gr.week_schedule)
        val_el = val_el + m.calc_goal_function_elements(end=True)
        val += m.calc_goal_fcn()
    val_el = val_el / len(groups)
    val /= len(groups)
    return val_el, val

