from typing import Iterable, Type, List, TYPE_CHECKING

from basic_structures import Group
from data import MIN_HOUR, MAX_HOUR

from time_ import TimeDelta as TD, Time, TimeRange as TR
from utils.constans import DAYS

if TYPE_CHECKING:
    pass


def check_type_all(iterable: Iterable, type_: Type):
    return all(isinstance(element, type_) for element in iterable)


def check_if_time_is_available(times: Iterable["Time"]):
    if not all(map(lambda time: MIN_HOUR <= time <= MAX_HOUR, times)):
        raise ValueError("Time outside time limits")


def filter_times_grater_or_equal_than(times: List["TR"], time_delta: "TD"):
    return tuple(filter(lambda time: time.dur >= time_delta, times))


# testme
def _get_common_ranges_from_two(one: List["TR"], other: List["TR"]):
    commons = []
    for one_tr in one:
        for other_tr in other:
            common = (_get_common_range(one_tr, other_tr))
            commons.extend(common)
    return commons


# testme
def _get_common_range(self: "TR", other: "TR") -> List["TR"]:
    commons = []
    if self.intersect(other):
        times = [self.start, self.end, other.start, other.end]
        times.sort()
        for i in range(2):
            tr = TR(start=times[i], end=times[i+1], day=self.day)
            if tr.intersect(self) and tr.intersect(other):
                commons.append(tr)
    return commons


# testme
def _merge_touching_ranges_in_day(ranges: List["TR"]):
    ranges = sorted(ranges, key=lambda tr: tr.start)
    merged = []

    if len(ranges) == 0:
        return merged

    prev_range = ranges[0]
    for range_ in ranges[1:]:
        if prev_range.end == range_.start:
            prev_range = TR(prev_range.start, range_.end, day=range_.day)
        else:
            merged.append(prev_range)
            prev_range = range_
    merged.append(prev_range)
    return merged


# testme
def _get_common_ranges_for_day(time_ranges_list: List[List["TR"]],
                               min_dur: TD):
    prev_trs = time_ranges_list[0]
    for trs in time_ranges_list[1:]:
        ranges = _get_common_ranges_from_two(prev_trs, trs)
        prev_trs = _merge_touching_ranges_in_day(ranges)
        prev_ranges_anough_wide = filter_times_grater_or_equal_than(prev_trs,
                                                                    min_dur)
    return prev_trs


# testme
def get_ranges_from_week_schedule(groups: List[Group], min_dur: TD):
    week_ranges = []
    for day in DAYS:
        day_ranges = []
        for group in groups:
            ranges = group.week_schedule.days[day].get_free_times()
            day_ranges.append(ranges)
        week_ranges.append(_get_common_ranges_for_day(day_ranges, min_dur))






