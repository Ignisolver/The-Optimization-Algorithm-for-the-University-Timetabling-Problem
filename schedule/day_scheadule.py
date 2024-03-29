from dataclasses import dataclass, field
from functools import cache
from typing import Iterator, List, TYPE_CHECKING, Union

from data_generation.basic_config import MIN_HOUR, MAX_HOUR, \
    MAX_TIME_PER_DAY
from time_ import TimeDelta, TimeRange, Time
from utils.distanses_manager import Distances
from utils.types_ import ClassesType as CT, Day

if TYPE_CHECKING:
    from algorithm.best_times_finder import Start
    from basic_structures import Classes


@dataclass
class DaySchedule:
    day: Day
    _classes: List["Classes"] = field(default_factory=list)
    _temp_cl_nr: int | None = None
    _distances: Distances = Distances()
    _changed: bool = True
    _last_val: int = 0

    def __len__(self) -> int:
        """
        return time of classes in minutes
        """
        total_time = int(sum([cl.dur for cl in self._classes], TimeDelta()))
        total_time -= int(self.get_unavailable_len())
        return total_time

    def __iter__(self) -> Iterator:
        return iter(self._classes)

    def __repr__(self):
        return str(self._classes)

    def get_classes(self) -> List["Classes"]:
        return self._classes

    def get_last_classes(self) -> Union["Classes", None]:
        if len(self._classes) == 0:
            return None
        return self._classes[-1]

    def get_last_classes_before(self, time: Time) -> Union["Classes", None]:
        last_cl = None
        if len(self._classes) == 0:
            return last_cl

        for cl in reversed(self._classes):
            if cl.start_time < time:
                last_cl = cl
                break
        return last_cl

    def get_next_classes_after(self, time: Time) -> Union["Classes", None]:
        if len(self._classes) == 0:
            return None
        next_cl = None
        for cl in self._classes:
            if cl.start_time >= time:
                next_cl = cl
                break
        return next_cl

    def get_first_classes(self) -> Union["Classes", None]:
        if len(self._classes) == 0:
            return None
        return self._classes[0]

    def get_amount_of_labs(self) -> int:
        am = sum(1 for cl in self._classes if cl.classes_type == CT.LABORATORY)
        return am

    def get_amount_of_lectures(self) -> int:
        am = sum(1 for cl in self._classes if cl.classes_type == CT.LECTURE)
        return am

    def get_amount_of_classes(self) -> int:
        am = sum(1 for cl in self._classes
                 if cl.classes_type != CT.UNAVAILABLE)
        return am

    def temp_assign(self, classes: "Classes"):
        self.assign(classes)
        self._temp_cl_nr = self._classes.index(classes)

    def unassign_temp(self):
        del self._classes[self._temp_cl_nr]
        self._temp_cl_nr = None

    @staticmethod
    def _sort_classes_fcn(classes):
        return classes.start_time

    def _sort_classes(self):
        self._classes.sort(key=self._sort_classes_fcn)

    def assign(self, classes: "Classes"):
        self._assert_assignment_available(classes)
        self._classes.append(classes)
        self._sort_classes()
        self._changed = True

    def pretty_represent(self):
        s = " "
        print(f"{3 * s}ID | start ->{2 * s}end{2 * s}| {'TYPE':^11}| NAME")
        print(
            2 * s + 4 * "-" + "|" + 16 * '-' + '|' + 12 * '-' + "|" + 10 * '-')
        for cl in self._classes:
            print(cl.pretty_represent())

    def get_free_time(self, max_h=MAX_HOUR, min_h=MIN_HOUR) -> "TimeDelta":
        """time between min and max hour without classes and move time"""
        time_before = self._classes[0].start_time - min_h
        time_after = max_h - self._classes[-1].end_time
        time_during = self.get_brake_time()
        time_unavail = self.get_unavailable_len()
        return time_before + time_during + time_after - time_unavail

    def get_free_times(self, max_h=MAX_HOUR,
                       min_h=MIN_HOUR) -> List["TimeRange"]:
        """with move time"""
        start_h = min_h
        times = []
        for cls_ in self._classes:
            end_h = cls_.start_time
            dur = end_h - start_h
            tr = TimeRange(start_h, start_h+dur, day=self.day)
            times.append(tr)
            start_h = cls_.end_time
        times.append(TimeRange(start_h, start_h + (max_h - start_h), day=self.day))
        times = list(filter(lambda tr: tr.dur != TimeDelta(), times))
        return times

    def get_unavailable_len(self):
        tot_time = TimeDelta()
        for cl in self._classes:
            if cl.classes_type == CT.UNAVAILABLE:
                tot_time += cl.dur
        return tot_time

    def _calc_time_btw_classes(self, earlier: "Classes",
                               later: "Classes",
                               move_time_enable=True) -> TimeDelta:
        if ((earlier.classes_type == CT.UNAVAILABLE or
                later.classes_type == CT.UNAVAILABLE) or
                (earlier is None) or
                (later is None)):
            return TimeDelta()
        total_t = later.start_time - earlier.end_time
        if move_time_enable:
            mov_t = self._distances[earlier.room, later.room]
        else:
            mov_t = TimeDelta()
        return total_t - mov_t

    def get_brake_time(self, move_time_enable=True) -> "TimeDelta":
        """without move time"""
        total_time = TimeDelta()
        if len(self._classes) <= 1:
            return total_time
        prev_cl = self._classes[0]
        for cl in self._classes[1:]:
            if cl.classes_type == CT.UNAVAILABLE:
                continue
            total_time += self._calc_time_btw_classes(prev_cl, cl,
                                                      move_time_enable)
            prev_cl = cl
        unavail_time = self.get_unavailable_len()
        return total_time - unavail_time

    def get_amount_of_classes_between(self, start_h, end_h):
        if self._changed:
            n = 0
            for cls_ in self._classes:
                if start_h <= cls_.start_time < end_h:  # to wystarczy bo zajęć nie skrócimy
                    if cls_.classes_type != CT.UNAVAILABLE:
                        n += 1
            self._last_val = n
            self._changed = False
            return n
        else:
            return self._last_val


    def is_space_not_busy(self, start: "Start", classes: "Classes"):
        tr = TimeRange(start.time, start.time+classes.dur)
        if self._is_time_range_intersect_any_classes(tr):
            return False
        return True

    def _is_time_range_intersect_any_classes(self, tr):
        for cl in self._classes:
            cl_tr = TimeRange(cl.start_time, cl.end_time)
            if cl_tr.intersect(tr):
                return True
        return False

    def _assert_not_intersect(self, new_cl: "Classes"):
        new_cl_tr = TimeRange(new_cl.start_time, new_cl.end_time)
        if self._is_time_range_intersect_any_classes(new_cl_tr):
            raise AssertionError

    def _assert_distance_is_not_to_short(self, new_cl: "Classes"):
        for cl in self._classes:
            td = None
            if new_cl.end_time <= cl.start_time:
                td = self._calc_time_btw_classes(new_cl, cl)
            elif cl.end_time <= new_cl.start_time:
                td = self._calc_time_btw_classes(cl, new_cl)
            if td is not None:
                assert td >= TimeDelta(0, 0)

    def _assert_assignment_available(self, new_cl: "Classes"):
        self._assert_not_intersect(new_cl)

    def is_too_long(self, dur: TimeDelta):
        return len(self) + int(dur) > MAX_TIME_PER_DAY
