from dataclasses import dataclass
from typing import Tuple, Union, TYPE_CHECKING, Iterator, List

from utils.types_ import ClassesType, ClassesId, Day, DAY_LETTER, get_color
from basic_structures.lecturer import Lecturer, UnavailableLecturer
from basic_structures.room import Room, UnavailabilityRoom
from time_ import Time, TimeDelta
if TYPE_CHECKING:
    from basic_structures import Group


@dataclass
class Classes:
    id_: ClassesId
    name: str
    dur: TimeDelta
    classes_type: ClassesType
    avail_rooms: Tuple[Room, ...]
    lecturer: "Lecturer"
    groups: Tuple["Group", ...]
    room: Room | None = None
    _start_time: Union[Time, None] = None
    _end_time: Union[Time, None] = None
    day: Day = None

    def assign(self,
               time: Time,
               room: Room,
               day: Day):
        self.room = room
        self.start_time = time
        self.day = day
        self._assign_to_room_groups_lecturer()

    def add_info_to_week_schedule(self):
        for item in self.get_with_schedules():
            item.week_schedule.classes_amount += 1
            item.week_schedule.classes_time += int(self.dur)

    def _assign_to_room_groups_lecturer(self):
        self.lecturer.assign(self)
        self.room.assign(self)
        for gr in self.groups:
            gr.assign(self)

    def temp_assign(self, time, day):
        self.start_time = time
        self.day = day
        try:
            self.lecturer.temp_assign(self)
        except:
            self.lecturer.week_schedule.days[day].pretty_represent()
            print(time, self.dur)
        for gr in self.groups:
            gr.temp_assign(self)

    # testme
    def get_sorted_rooms(self) -> List[Room]:
        return sorted(self.avail_rooms,
                      key=lambda r: r.occup_priority,
                      reverse=True)

    def unassign_temp(self):
        self._start_time = None
        self._end_time = None
        self.lecturer.unassign_temp()
        for gr in self.groups:
            gr.unassign_temp()

    def get_with_schedules(self):
        return self.groups + (self.lecturer,)

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @start_time.setter
    def start_time(self, start_time: Time):
        end_time = start_time + self.dur
        self._start_time = start_time
        self._end_time = end_time

    @start_time.deleter
    def start_time(self):
        self._start_time = None
        self._end_time = None

    def pretty_represent(self):
        id_ = f"{self.id_:>5}"
        start_time = f"{self.start_time.hour:>02}:{self.start_time.minute:>02}"
        end_time = f"{self.end_time.hour:>02}:{self.end_time.minute:>02}"
        name = f"{self.name}"
        type_ = self.classes_type
        s1 = f"{id_} | {start_time} -> {end_time} |"
        s2 = f"{type_:^12}| {name}"
        return s1 + s2

    def to_yaml(self):
        s = " "
        txt = f'\n{2 * s}'.join([f"- name: |",
                                 f"{2 * s}{self.name}",
                                 f"{2 * s}ID: {self.id_}",
                                 f"{2 * s}R: {self.room.name}",
                                 f"{2 * s}L: {self.lecturer.name}",
                                 f"{2 * s}G: {[g for g in self.groups]}",
                                 f"days: {DAY_LETTER[self.day]}",
                                 f"time: {self.start_time} - {self.end_time}",
                                 f"color: '{next(get_color)}'"])
        return txt

    def assign_occupacity(self):
        for room in self.avail_rooms:
            room.add_potential_classes(self)


class UnavailableClasses:
    def __new__(cls, id_: int, start: Time, dur: TimeDelta, day: Day):
        cl = Classes(id_=id_,
                     name="UNAVAILABLE",
                     dur=dur,
                     classes_type=ClassesType.UNAVAILABLE,
                     avail_rooms=(),
                     lecturer=UnavailableLecturer(),
                     groups=(),
                     day=day,
                     room=UnavailabilityRoom())
        cl.start_time = start
        return cl
