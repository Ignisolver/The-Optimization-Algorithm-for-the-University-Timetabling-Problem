from dataclasses import dataclass
from pickle import load, dump


@dataclass
class ClassesInfo1:
    lecturer: str
    name: str
    type: str
    room: str


@dataclass
class ClassesInfo2:
    start: tuple
    end: tuple
    tag: str
    group: str
    shortcut: str

@dataclass
class ClassesInfo:
    info_1: ClassesInfo1
    info_2: ClassesInfo2


def split_with(text, el, last=True):
    if last is False:
        ind = text.find(el)
        beg, end = text[:ind], text[ind + len(el):]
    else:
        ind = len(text) - text[::-1].find(el[::-1])
        beg, end = text[:ind - len(el)], text[ind:]
    return beg, end


def extract_div(text: str):
    name_type_, lecturers = split_with(text, "),", last=True)
    name_type_ = "".join(name_type_)
    lecturers = lecturers.split(",")
    lecturers = list(map(lambda x: x.strip(), lecturers))
    name, type_room = split_with(name_type_, " - ", last=True)
    name = "".join(name)
    name = name.strip()
    type_, room = split_with(type_room, "(")
    type = type_.strip()
    room = room[:-1]
    return ClassesInfo1(lecturers, name, type, room)


def extract_span(text: str):
    hours, tag_gr, shortcut = text.split(",")
    start_hour, end_hour = hours.split("-")
    s_h, s_m = start_hour.split(":")
    e_h, e_m = end_hour.split(":")
    s_h = int(s_h)
    s_m = int(s_m)
    e_h = int(e_h)
    e_m = int(e_m)
    tag_gr = tag_gr.strip()
    tag, gr = tag_gr.split(" ")
    shortcut = shortcut.strip()
    return ClassesInfo2((s_h, s_m), (e_h, e_m), tag, gr, shortcut)

if __name__ == '__main__':
    all_elements = []
    for i in range(1, 22):
        with open(f"all_classes_{i}.bin", "rb") as file:
            all_elements.extend(load(file))

    print(*all_elements, sep="\n")

    infos = []

    for el in all_elements:
        div, span = el
        print(div, span)
        try:
            i1 = extract_div(div)
            i2 = extract_span(span)
        except:
            print(div, span)
        else:
            infos.append(ClassesInfo(i1, i2))


    with open("extracted.bin", "wb") as file:
        dump(infos, file)


