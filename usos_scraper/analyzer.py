import pickle
from dataclasses import dataclass
from itertools import cycle
from pickle import load
from typing import List

from usos_scraper.extractor import ClassesInfo, ClassesInfo1, ClassesInfo2
from time_ import TimeDelta, Time


@dataclass
class ClassesData:
    name: str
    lecturer: str
    duration: TimeDelta
    type: str

if __name__ == "__main__":
    with open("extracted.bin", "rb") as file:
        infos: List[ClassesInfo] = load(file)

    print(len(infos))
    lecturers = []
    groups = []
    tags = []
    types = []
    rooms = []
    classes = []
    shortcuts = []

    lecture_rooms = []
    other_rooms = []

    lecturers_am = 0
    classes_am = 0

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
            lecturers_am +=1
        else:
            room = info.info_1.room
            if room != last_lab_room:
                other_rooms.append(room)
                last_lab_room = room
            t = "L"
            classes_am += 1

        cd = ClassesData(info.info_1.name, info.info_1.lecturer[0],
                         Time(*info.info_2.end) - Time(*info.info_2.start), t)
        classes_datas.append(cd)




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



    print("lecturers:", len(set_lecturers))
    print("groups:", len(set_groups))
    print("tags:", set_tags)
    print("types:", set_types)
    print("lab rooms:", len(other_rooms))
    print("lect rooms:", len(lecture_rooms))
    print("lectures:", lecturers_am)
    print("labs:", classes_am)
    print("classes:", len(classes))
    print("shortcuts:", len(set_shortcuts))

    lecture_persons = []
    lab_persons = []
    lab_durations = []
    lect_durations = []
    for cl in classes_datas:
        if cl.type == "W":
            lecture_persons.append(cl.lecturer)
            dur = TimeDelta(0, int(cl.duration))
            lect_durations.append(dur)
        else:
            lab_persons.append(cl.lecturer)
            dur = TimeDelta(0, int(cl.duration))
            lab_durations.append(dur)

    with open("lect_p.bin", "wb") as file:
        pickle.dump(cycle(lecture_persons), file)

    with open("lect_d.bin", "wb") as file:
        pickle.dump(cycle(lect_durations), file)

    with open("lab_p.bin", "wb") as file:
        pickle.dump(cycle(lab_persons), file)

    with open("lab_d.bin", "wb") as file:
        pickle.dump(cycle(lab_durations), file)

