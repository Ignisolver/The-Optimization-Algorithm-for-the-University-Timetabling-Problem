from abc import ABC

from yaml import safe_load

from basic_structures import Group, Room, Classes, Lecturer
from data_input.basic_structure_loader_utils import PrimitiveTimeLoader, BasicStructureLoaderPrimitive
from data_input.input_types import InputStructureType, Tag
from utils.types_ import ClassesType, GroupId, RoomId, ClassesId, LecturerId
from collections import namedtuple

PreferredTime = namedtuple("PreferredTime", ("time_range", "points"))


class YamlLoader:
    @staticmethod
    def _get_yaml_str_from_file(file_path: str):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        text = "".join(lines)
        return text

    @staticmethod
    def _load_data_from_yaml_string(yaml_str: str):
        return safe_load(yaml_str)


class BasicStructureLoader(BasicStructureLoaderPrimitive, ABC):
    def __init__(self):
        self.yaml_loader = YamlLoader()
        self.time_loader = PrimitiveTimeLoader()

    def _load_group(self, data: dict) -> Group:
        id_, name = self._load_id_and_name(data, InputStructureType.Group)

        amount_of_students = data[Tag.AMOUNT_OF_STUDENTS]
        self._assert_positive_int(amount_of_students)

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
        self._assert_positive_int(capacity)

        available_times, unavailable_times = self.time_loader.load_available_and_unavailable_times(data)

        room = Room(RoomId(id_),
                    name=name,
                    _initial_availability_minutes=0,
                    people_capacity=capacity)

        # todo initial_occupation, available_times
        return room

    def _load_classes(self, data: dict) -> Classes:
        id_, name = self._load_id_and_name(data, InputStructureType.Classes)

        duration = data[Tag.DURATION]
        self._assert_positive_int(duration)

        classes_type = ClassesType(data[Tag.CLASSES_TYPE])

        rooms = data[Tag.AVAILABLE_ROOMS]
        self._assert_correct_ids_tuple(rooms)

        groups = data[Tag.GROUPS]
        self._assert_correct_ids_tuple(groups)

        lecturers = data[Tag.LECTURERS]
        self._assert_correct_ids_tuple(lecturers)

        classes = Classes(ClassesId(id_), name, duration, classes_type, rooms, lecturers, groups)

        return classes

    def _load_lecturer(self, data: dict) -> Lecturer:
        id_, name = self._load_id_and_name(data, InputStructureType.Lecturer)

        available_times, unavailable_times = self.time_loader.load_available_and_unavailable_times(data)

        preferred_times = self.time_loader.load_preferred_times(data[Tag.PREFERRED_TIMES])

        lecturer = Lecturer(LecturerId(id_),
                            name)

        # todo preferred and available times

        return lecturer

    def load_all(self, folder_abs_path):
        pass

    # todo iter thru folders and files
    # todo tests

















