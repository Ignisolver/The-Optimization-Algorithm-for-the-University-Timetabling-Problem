from dataclasses import dataclass, field
from typing import Iterator, List, TYPE_CHECKING, Union

from data import MIN_HOUR, MAX_HOUR
from tools.distanses_manager import DISTANCES, Distances
from utils.types_ import ClassesType as CT
from time_ import TimeDelta, TimeRange, Time

if TYPE_CHECKING:
    from basic_structures import Classes


@dataclass
class DaySchedule:
    day_number: int
    _classes: List["Classes"] = field(default_factory=list)
    _temp_cl_nr: int = None
    _distances: Distances = DISTANCES

    def __len__(self) -> int:
        """
        return time of classes in minutes
        """
        total_time = int(sum([cl.dur for cl in self._classes], TimeDelta()))
        return total_time

    def __iter__(self) -> Iterator:
        return iter(self._classes)

    def get_classes(self) -> List["Classes"]:
        return self._classes

    def get_last_classes(self) -> Union["Classes", None]:
        if len(self._classes) == 0:
            return None
        return self._classes[-1]

    def get_last_classes_before(self, time: Time) -> Union["Classes", None]:
        if len(self._classes) == 0:
            return None
        last_cl = None
        for cl in self._classes:
            if cl.start_time < time:
                last_cl = cl
            else:
                break
        return last_cl

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
        return len(self._classes)

    def temp_assign(self, classes: "Classes"):
        self.assign_classes(classes)
        self._temp_cl_nr = self._classes.index(classes)

    def revert_temp_assign(self):
        del self._classes[self._temp_cl_nr]
        self._temp_cl_nr = None

    @staticmethod
    def _sort_classes_fcn(classes):
        return classes.start_time

    def _sort_classes(self):
        self._classes.sort(key=self._sort_classes_fcn)

    def assign_classes(self, classes: "Classes"):
        self._assert_assignment_available(classes)
        self._classes.append(classes)
        self._sort_classes()

    def pretty_represent(self):
        s = " "
        print(f"{3*s}ID | start ->{2*s}end{2*s}| LAB/LECT{3*s}| NAME")
        print(2*s + 4 *"-"+"|"+16*'-'+'|'+12*'-'+"|"+10*'-')
        for cl in self._classes:
            cl.pretty_represent()

    def get_free_time(self, max_h=MAX_HOUR, min_h=MIN_HOUR) -> "TimeDelta":
        """time between min and max hour without classes and move time"""
        time_before = self._classes[0].start_time - min_h
        time_after = max_h - self._classes[-1].end_time
        time_during = self.get_brake_time()
        return time_before + time_during + time_after

    def _calc_time_btw_classes(self, earlier: "Classes", later: "Classes"):
        """without move time"""
        total_t = later.start_time - earlier.end_time
        mov_t = self._distances[earlier.assigned_room, later.assigned_room]
        return total_t - mov_t

    def get_brake_time(self) -> "TimeDelta":
        """without move time"""
        total_time = TimeDelta()
        last_cl = self._classes[0]
        for cl in self._classes[1:]:
            total_time += self._calc_time_btw_classes(last_cl, cl)
            last_cl = cl
        return total_time

    def _assert_not_intersect(self, new_cl):
        new_cl_tr = TimeRange(new_cl.start_time, new_cl.end_time)
        for cl in self._classes:
            cl_tr = TimeRange(cl.start_time, cl.end_time)
            assert not cl_tr.intersect(new_cl_tr)

    def _assert_distance_is_not_to_long(self, new_cl):
        for cl in self._classes:
            td = None
            if new_cl.end_time <= cl.start_time:
                td = self._calc_time_btw_classes(new_cl, cl)
            elif cl.end_time <= new_cl.start_time:
                td = self._calc_time_btw_classes(cl, new_cl)
            if td is not None:
                assert td >= TimeDelta(0, 0)

    def _assert_assignment_available(self, new_cl):
        self._assert_not_intersect(new_cl)
        self._assert_distance_is_not_to_long(new_cl)




