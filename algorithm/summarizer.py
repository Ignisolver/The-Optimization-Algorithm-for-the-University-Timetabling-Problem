from dataclasses import dataclass
from math import floor
from typing import List

from algorithm.goal_function import Metric, GFV
from basic_structures import Group
from basic_structures.with_schedule import WithSchedule
from data_generation.generation_configs import MAX_TIME_PER_DAY
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
    all_items = (all_.groups, all_.lecturers, all_.rooms)
    names = ("GROUPS    :", "LECTURERS :", "ROOMS     : ")
    for name, items in zip(names, all_items):
        over_doable_hours = calc_over_doability_time(items)
        aval_time = calc_av_time_before(items)
        represent_before(name, over_doable_hours, aval_time)


def summarize_after(all_: All, alg_res):
    print(alg_res)
    gfv_el, val = calc_goal_function_val(all_.groups)
    print(gfv_el, end='')
    print(30*"-")
    print(f"MEDIUM GOAL FUNCTION VALUE: {val}")
    classes_time = sum(int(classes.dur) for classes in all_.classes)
    all_items = (all_.groups, all_.lecturers, all_.rooms)
    names = ("GROUPS    :", "LECTURERS :", "ROOMS     : ")
    print(30 * "-")
    for name, items in zip(names, all_items):
        available_time = calc_av_time(items)
        represent_after(classes_time, available_time, name)


def calc_av_time(items: List[WithSchedule]):
    return sum(it.week_schedule.available_time for it in items)


def calc_av_time_before(items: List[WithSchedule]):
    for item in items:
        item.week_schedule.calc_over_time_avail_time()
    all_free_time = sum(it.week_schedule.available_time for it in items)/60
    return all_free_time


def calc_over_doability_time(items: List[WithSchedule]):
    for item in items:
        item.week_schedule.calc_over_time_avail_time()
    return floor(sum(it.week_schedule.over_doable for it in items) / 60)


def represent_after(classes_time, available_time, name):
    leave_free_time = round(classes_time/available_time * 100, 1)
    print(name,
          f"{leave_free_time:4>} % time occupied")


def represent_before(name, over_doable_hours, max_time):
    if over_doable_hours >= 0:
        usage = round((1 + over_doable_hours/max_time) * 100, 2)
        print(name,
              f"RESOURCE USAGE: {usage} | ",
              f"{over_doable_hours} hours unassignable")
    else:
        usage = round((1 + over_doable_hours / max_time) * 100, 2)
        print(name,
              f"RESOURCE USAGE: {usage} % | ",
              f"{-over_doable_hours} hours free over needed")


def calc_goal_function_val(groups: List[Group]):
    val_el = GFV(0, 0, 0, 0)
    val = 0
    for gr in groups:
        m = Metric(gr.week_schedule)
        val_el = val_el + m.calc_goal_function_elements()
        val += m.calc_goal_fcn()
    val_el = val_el / len(groups)
    val /= len(groups)
    return val_el, val

