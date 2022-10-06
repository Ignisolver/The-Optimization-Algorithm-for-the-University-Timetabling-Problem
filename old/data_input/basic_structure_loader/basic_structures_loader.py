from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple, List, Callable

from basic_structures import Group, Room, Classes, Lecturer
from old.data_input.basic_structure_loader.basic_structure_loader_utils.time_loader import TimeLoader
from old.data_input.basic_structure_loader.basic_structure_loader_utils.basic_structure_loader_primitive import BasicStructureLoaderPrimitive
from old.data_input.basic_structure_loader.basic_structure_loader_utils.yaml_loader import YamlLoader
from old.data_input.basic_structure_loader.basic_structure_loader_utils.input_types import InputStructureType, Tag, FolderNames
from utils.types_ import ClassesType, GroupId, RoomId, ClassesId, LecturerId


@dataclass
class BasicStructures:
    lecturers: List[Lecturer] = field(default_factory=list)
    groups: List[Group] = field(default_factory=list)
    classes: List[Classes] = field(default_factory=list)
    rooms: List[Room] = field(default_factory=list)


class BasicStructureLoader(BasicStructureLoaderPrimitive, ABC):
    def __init__(self):
        self.yaml_loader = YamlLoader()
        self.time_loader = TimeLoader()

    def _load_group(self, data: dict) -> Group:
        id_, name = self._load_id_and_name(data, InputStructureType.Group)

        amount_of_students = data[Tag.AMOUNT_OF_STUDENTS]
        self._assert_not_negative_int(amount_of_students)

        classes_to_assign = data[Tag.CLASSES_TO_ASSIGN]
        self._assert_correct_ids_tuple(classes_to_assign)

        group = Group(GroupId(id_),
                      name=name,
                      amount_of_students=amount_of_students,
                      _unassigned_classes=classes_to_assign)
        return group

    def _load_room(self, data: dict) -> Room:
        id_, name = self._load_id_and_name(data, InputStructureType.Room)

        capacity = data[Tag.CAPACITY]
        self._assert_not_negative_int(capacity)

        building_id = data[Tag.BUILDING_ID]
        self._assert_not_negative_int(building_id)

        av = data[Tag.AVAILABLE_TIMES]
        unav = data[Tag.UNAVAILABLE_TIMES]
        av_times, unav_times = self.time_loader.load_times(av, unav)

        room = Room(RoomId(id_),
                    name=name,
                    building_id=building_id,
                    _initial_availability_minutes=0,
                    people_capacity=capacity)

        # todo initial_occupation <- available_times
        return room

    def _load_classes(self, data: dict) -> Classes:
        id_, name = self._load_id_and_name(data, InputStructureType.Classes)

        duration = data[Tag.DURATION]
        self._assert_not_negative_int(duration)

        classes_type = ClassesType(data[Tag.CLASSES_TYPE])

        rooms = data[Tag.AVAILABLE_ROOMS]
        self._assert_correct_ids_tuple(rooms, False)

        groups = data[Tag.GROUPS]
        self._assert_correct_ids_tuple(groups, False)

        lecturers = data[Tag.LECTURERS]
        self._assert_correct_ids_tuple(lecturers, False)

        classes = Classes(ClassesId(id_), name, duration, classes_type, rooms,
                          lecturers, groups)

        return classes

    def _load_lecturer(self, data: dict) -> Lecturer:
        id_, name = self._load_id_and_name(data, InputStructureType.Lecturer)

        available_times, unavailable_times = self.time_loader.load_times(
            data[Tag.AVAILABLE_TIMES], data[Tag.UNAVAILABLE_TIMES])

        preferred_times = self.time_loader.load_pref_times(
            data[Tag.PREFERRED_TIMES])

        lecturer = Lecturer(LecturerId(id_),
                            name)

        # todo preferred and available times

        return lecturer

    def _select_method_and_container(self,
                                     folder_name: str,
                                     basic_structures: BasicStructures) -> \
            Tuple[Callable,
                  List]:
        match folder_name:
            case FolderNames.CLASSES:
                method = self._load_classes
                container = basic_structures.classes
            case FolderNames.GROUPS:
                method = self._load_group
                container = basic_structures.groups
            case FolderNames.LECTURERS:
                method = self._load_lecturer
                container = basic_structures.lecturers
            case FolderNames.ROOMS:
                method = self._load_room
                container = basic_structures.rooms
            case _:
                raise FileNotFoundError("Folders ")

        return method, container

    def _load_structure(self,
                        method: Callable,
                        container: List,
                        file_path: Path):
        data = self.yaml_loader.load_data_from_yaml_file(file_path)
        structure = method(data)
        container.append(structure)

    def load_all(self,
                 folder_abs_raw_path: Path) -> BasicStructures:
        basic_structures = BasicStructures()
        for structure_folder_path in folder_abs_raw_path.glob('*'):
            method, container = self._select_method_and_container(
                structure_folder_path.name, basic_structures)
            for file_path in structure_folder_path.glob('*'):
                self._load_structure(method, container, file_path)
        return basic_structures
