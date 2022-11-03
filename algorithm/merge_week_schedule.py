from typing import List, Tuple

from basic_structures.with_schedule import WithSchedule
from time_ import TimeRange as TR, TimeDelta as TD
from utils.constans import DAYS


def _filter_ranges_grater_or_equal_than(times: List["TR"], time_delta: "TD"):
    return list(filter(lambda time: time.dur >= time_delta, times))


def _get_common_ranges(self: "TR", other: "TR") -> List["TR"]:
    commons = []
    if self.intersect(other):
        times = [self.start, self.end, other.start, other.end]
        times.sort()
        for i in range(2):
            tr = TR(start=times[i], end=times[i+1], day=self.day)
            if tr.intersect(self) and tr.intersect(other) and tr.dur != TD():
                commons.append(tr)
    return commons


def _get_common_ranges_from_two_list(one: List["TR"], other: List["TR"]):
    commons = []
    for one_tr in one:
        for other_tr in other:
            common = _get_common_ranges(one_tr, other_tr)
            commons.extend(common)
    return commons


def _merge_touching_available_ranges_in_day(ranges: List["TR"]):
    merged = []

    if len(ranges) == 0:
        return merged

    ranges = sorted(ranges, key=lambda tr: tr.start)

    prev_range = ranges[0]
    for range_ in ranges[1:]:
        if prev_range.end == range_.start:
            prev_range = TR(prev_range.start, range_.end, day=range_.day)
        else:
            merged.append(prev_range)
            prev_range = range_
    merged.append(prev_range)
    return merged


def _get_common_ranges_for_day(time_ranges_list: List[List["TR"]],
                               min_dur: TD) -> List["TR"]:
    prev_trs = time_ranges_list[0]
    for trs in time_ranges_list[1:]:
        ranges = _get_common_ranges_from_two_list(prev_trs, trs)
        prev_trs = _merge_touching_available_ranges_in_day(ranges)
        prev_ranges_enough_wide = _filter_ranges_grater_or_equal_than(prev_trs,
                                                                      min_dur)
        prev_trs = prev_ranges_enough_wide
    return prev_trs


def get_free_ranges_from_week_schedules(items: Tuple[WithSchedule],
                                         min_dur: TD):
    week_ranges = []
    for day in DAYS:
        day_ranges = []
        for item in items:
            ranges = item.week_schedule.days[day].get_free_times()
            day_ranges.append(ranges)
        week_ranges.extend(_get_common_ranges_for_day(day_ranges, min_dur))
    return week_ranges
