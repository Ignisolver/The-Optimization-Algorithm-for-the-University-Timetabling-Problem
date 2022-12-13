import pickle
from dataclasses import dataclass
from pickle import load
from typing import List

from extractor import ClassesInfo, ClassesInfo1, ClassesInfo2
from time_ import TimeDelta, Time

with open("extracted.bin", "rb") as file:
    infos: List[ClassesInfo] = load(file)

lecturers = []
groups = []
tags = []
types = []
rooms = []
classes = []
shortcuts = []

lecture_rooms = []
other_rooms = []


@dataclass
class ClassesData:
    name: str
    lecturer: str
    duration: TimeDelta
    type: str

classes_datas = []
last_lab_room = None
last_lect_room = None
for info in infos:
    classes.append(info.info_1.name)
    room = info.info_1.room
    lecturers.append(info.info_1.lecturer)
    types.append(info.info_1.type)
    tags.append(info.info_2.tag)
    shortcuts.append(info.info_2.shortcut)
    groups.append(info.info_2.group)
    if info.info_2.tag == "W" or info.info_2.tag == "WF":
        room = info.info_1.room
        if room != last_lect_room:
            lecture_rooms.append(room)
            last_lect_room = room
        t = "W"
    else:
        room = info.info_1.room
        if room != last_lab_room:
            other_rooms.append(room)
            last_lab_room = room
        t = "L"

    cd = ClassesData(info.info_1.name, info.info_1.lecturer[0],
                     Time(*info.info_2.end) - Time(*info.info_2.start), t)
    classes_datas.append(cd)

with open("classes_data.bin", "wb") as file:
    pickle.dump(classes_datas, file)


set_lecturers = set()
for el in lecturers:
    for l in el:
        set_lecturers.add(l)
set_groups = set()
for el in groups:
    set_groups.add(el)
set_tags = set()
for el in tags:
    set_tags.add(el)
set_types = set()
for el in types:
    set_types.add(el)
print(*rooms, sep="\n")
set_rooms = set()
for el in rooms:
    set_rooms.add(el)
set_shortcuts = set()
for el in shortcuts:
    set_shortcuts.add(el)

lecturers_am = len(lecture_rooms)
classes_am = len(other_rooms)

print("lecturers:", len(set_lecturers))
print("groups:", len(set_groups))
print("tags:", set_tags)
print("types:", set_types)
print("lab rooms:", len(other_rooms))
print("lect rooms:", len(lecture_rooms))
print("lectures:", len(lecture_rooms))
print("labs:", len(other_rooms))
print("classes:", len(classes))
print("shortcuts:", len(set_shortcuts))