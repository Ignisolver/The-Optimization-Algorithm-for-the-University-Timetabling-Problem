from pathlib import Path
from typing import List

import pytest

from old.data_input.basic_structure_loader.basic_structure_loader_utils.input_types import \
    FolderNames
from old.data_input import \
    BasicStructureLoader, BasicStructures
from utils.types_ import ClassesType


@pytest.fixture(scope="function")
def bsl() -> BasicStructureLoader:
    return BasicStructureLoader()


def get_path_to_sth_in_data_folder(sth_name):
    path = Path(__file__).parent.joinpath("data").joinpath(sth_name).absolute()
    return path


class TestBasicStructureLoader:
    def test__load_group__ok(self, bsl):
        group_data = {"TYPE": "Group",
                      "ID": 88,
                      "NAME": "gr_name",
                      "AMOUNT_OF_STUDENTS": 77,
                      'CLASSES_TO_ASSIGN': [1, 3, 4]}
        group = bsl._load_group(group_data)
        assert group.name == "gr_name"
        assert group.id_ == 88
        assert group.amount_of_students == 77
        assert group._unassigned_classes == [1, 3, 4]

    def test__load_group___incorrect_type(self, bsl):
        group_data = {"TYPE": "Lecturer",
                      "ID": 88,
                      "NAME": "gr_name",
                      "AMOUNT_OF_STUDENTS": 77,
                      'CLASSES_TO_ASSIGN': [1, 3, 4]}
        with pytest.raises(AssertionError):
            _ = bsl._load_group(group_data)

    def test__load_group___incorrect_id(self, bsl):
        group_data = {"TYPE": "Group",
                      "ID": None,
                      "NAME": "gr_name",
                      "AMOUNT_OF_STUDENTS": 77,
                      'CLASSES_TO_ASSIGN': [1, 3, 4]}
        with pytest.raises(AssertionError):
            _ = bsl._load_group(group_data)

    def test__load_group___incorrect_amount_of_students(self, bsl):
        group_data = {"TYPE": "Lecturer",
                      "ID": 88,
                      "NAME": "gr_name",
                      "AMOUNT_OF_STUDENTS": "dsds",
                      'CLASSES_TO_ASSIGN': [1, 3, 4]}
        with pytest.raises(AssertionError):
            _ = bsl._load_group(group_data)

    def test__load_group___incorrect_classes_to_assign(self, bsl):
        group_data = {"TYPE": "Lecturer",
                      "ID": 88,
                      "NAME": "gr_name",
                      "AMOUNT_OF_STUDENTS": 77,
                      'CLASSES_TO_ASSIGN': [1, 3, 3, -1, 4]}
        with pytest.raises(AssertionError):
            _ = bsl._load_group(group_data)

    def test__load_room__ok(self, bsl):
        room_data = {"TYPE": "Room",
                     "ID": 0,
                     "NAME": "r_name",
                     "CAPACITY": 30,
                     "BUILDING_ID": 12,
                     "AVAILABLE_TIMES": [[1, [10, 30], [12, 35]],
                                         [4, [11, 30], [15, 16]]],
                     "UNAVAILABLE_TIMES": None}
        room = bsl._load_room(room_data)
        assert room.name == "r_name"
        assert room.id_ == 0
        assert room.people_capacity == 30
        assert room.build_id == 12
        # todo available times

    def test__load_room__incorrect_type(self, bsl):
        room_data = {"TYPE": "Group",
                     "ID": 0,
                     "NAME": "r_name",
                     "CAPACITY": 30,
                     "AVAILABLE_TIMES": [[1, [10, 30], [12, 35]],
                                         [4, [11, 30], [15, 16]]],
                     "UNAVAILABLE_TIMES": None}
        with pytest.raises(AssertionError):
            _ = bsl._load_room(room_data)

    def test__load_room__incorrect_id(self, bsl):
        room_data = {"TYPE": "Room",
                     "ID": "p",
                     "NAME": "r_name",
                     "CAPACITY": 30,
                     "AVAILABLE_TIMES": [[1, [10, 30], [12, 35]],
                                         [4, [11, 30], [15, 16]]],
                     "UNAVAILABLE_TIMES": None}
        with pytest.raises(AssertionError):
            _ = bsl._load_room(room_data)

    def test__load_room__incorrect_capacity(self, bsl):
        room_data = {"TYPE": "Room",
                     "ID": 4,
                     "NAME": "r_name",
                     "CAPACITY": None,
                     "AVAILABLE_TIMES": [[1, [10, 30], [12, 35]],
                                         [4, [11, 30], [15, 16]]],
                     "UNAVAILABLE_TIMES": None}
        with pytest.raises(AssertionError):
            _ = bsl._load_room(room_data)

    def test__load_room__incorrect_building(self, bsl):
        room_data = {"TYPE": "Room",
                     "ID": 0,
                     "NAME": "r_name",
                     "CAPACITY": 30,
                     "BUILDING_ID": 12,
                     "AVAILABLE_TIMES": [[1, [10, 30], [12, 35]],
                                         [4, [11, 30], [15, 16]]],
                     "UNAVAILABLE_TIMES": None}
        room = bsl._load_room(room_data)
        assert room.name == "r_name"
        assert room.id_ == 0
        assert room.people_capacity == 30
        with pytest.raises(AssertionError):
            assert room.build_id == "ds"

    def test__load_room__incorrect_times(self, bsl):
        assert False

    def test__load_classes__ok(self, bsl):
        classes_data = {"TYPE": "Classes",
                        "ID": 0,
                        "NAME": "87654",
                        "DURATION": 15,
                        "CLASSES_TYPE": "W-N-2",
                        "AVAILABLE_ROOMS": [10, 20],
                        "GROUPS": [10, 44, 502],
                        "LECTURERS": [14, 25]}
        classes = bsl._load_classes(classes_data)
        assert classes.id_ == 0
        assert classes.name == "87654"
        assert classes.dur == 15
        assert classes.classes_type == ClassesType("W-N-2")
        assert classes.avail_rooms == [10, 20]
        assert classes.groups == [10, 44, 502]
        assert classes.avail_lecturers == [14, 25]

    def test__load_classes__incorrect_type(self, bsl):
        classes_data = {"TYPE": "Room",
                        "ID": 0,
                        "NAME": "87654",
                        "DURATION": 15,
                        "CLASSES_TYPE": "W-N-2",
                        "AVAILABLE_ROOMS": [10, 20],
                        "GROUPS": [10, 44, 502],
                        "LECTURERS": [14, 25]}
        with pytest.raises(AssertionError):
            _ = bsl._load_classes(classes_data)

    def test__load_classes__incorrect_id(self, bsl):
        classes_data = {"TYPE": "Classes",
                        "ID": "d",
                        "NAME": "87654",
                        "DURATION": 15,
                        "CLASSES_TYPE": "W-N-2",
                        "AVAILABLE_ROOMS": [10, 20],
                        "GROUPS": [10, 44, 502],
                        "LECTURERS": [14, 25]}
        with pytest.raises(AssertionError):
            _ = bsl._load_classes(classes_data)

    def test__load_classes__incorrect_duration(self, bsl):
        classes_data = {"TYPE": "Classes",
                        "ID": 5,
                        "NAME": "87654",
                        "DURATION": -10,
                        "CLASSES_TYPE": "W-N-2",
                        "AVAILABLE_ROOMS": [10, 20],
                        "GROUPS": [10, 44, 502],
                        "LECTURERS": [14, 25]}
        with pytest.raises(AssertionError):
            _ = bsl._load_classes(classes_data)

    def test__load_classes__incorrect_classes_type(self, bsl):
        classes_data = {"TYPE": "Classes",
                        "ID": 5,
                        "NAME": "87654",
                        "DURATION": 103,
                        "CLASSES_TYPE": "W-L-2",
                        "AVAILABLE_ROOMS": [10, 20],
                        "GROUPS": [10, 44, 502],
                        "LECTURERS": [14, 25]}
        with pytest.raises(ValueError):
            _ = bsl._load_classes(classes_data)

    def test__load_classes__incorrect_aval_rooms(self, bsl):
        classes_data = {"TYPE": "Classes",
                        "ID": 5,
                        "NAME": "87654",
                        "DURATION": 103,
                        "CLASSES_TYPE": "W-E-2",
                        "AVAILABLE_ROOMS": [],
                        "GROUPS": [10, 44, 502],
                        "LECTURERS": [14, 25]}
        with pytest.raises(AssertionError):
            _ = bsl._load_classes(classes_data)

    def test__load_classes__incorrect_aval_groups(self, bsl):
        classes_data = {"TYPE": "Classes",
                        "ID": 5,
                        "NAME": "87654",
                        "DURATION": 103,
                        "CLASSES_TYPE": "W-E-2",
                        "AVAILABLE_ROOMS": [22],
                        "GROUPS": [10, 44, 44, 502],
                        "LECTURERS": [14, 25]}
        with pytest.raises(AssertionError):
            _ = bsl._load_classes(classes_data)

    def test__load_classes__incorrect_lecturers(self, bsl):
        classes_data = {"TYPE": "Classes",
                        "ID": 5,
                        "NAME": "87654",
                        "DURATION": 103,
                        "CLASSES_TYPE": "W-E-2",
                        "AVAILABLE_ROOMS": [22],
                        "GROUPS": [10, 44, 502]}
        with pytest.raises(KeyError):
            _ = bsl._load_classes(classes_data)

    def test__load_lecturer__ok(self, bsl):
        lecturer_data = {"TYPE": "Lecturer",
                         "ID": 0,
                         "NAME": "Jan Kowalski",
                         "UNAVAILABLE_TIMES":
                             [[1, [10, 30], [12, 35]],
                              [2, [11, 30], [15, 16]]],

                         "AVAILABLE_TIMES": None,

                         "PREFERRED_TIMES":
                             [[[1, [10, 30], [12, 35]], 3],
                              [[3, [10, 30], [12, 35]], 6],
                              [None, 5]]}
        lecturer = bsl._load_lecturer(lecturer_data)
        assert lecturer.id_ == 0
        assert lecturer.name == "Jan Kowalski"
        # todo times

    def test__load_lecturer__incorrect_id(self, bsl):
        lecturer_data = {"TYPE": "Lecturer",
                         "ID": '11',
                         "NAME": "Jan Kowalski",
                         "UNAVAILABLE_TIMES":
                             [[1, [10, 30], [12, 35]],
                              [2, [11, 30], [15, 16]]],

                         "AVAILABLE_TIMES": None,

                         "PREFERRED_TIMES":
                             [[[1, [10, 30], [12, 35]], 3],
                              [[3, [10, 30], [12, 35]], 6],
                              [None, 5]]}
        with pytest.raises(AssertionError):
            _ = bsl._load_lecturer(lecturer_data)

    def test__load_lecturer__incorrect_type(self, bsl):
        lecturer_data = {"TYPE": "Classes",
                         "ID": 11,
                         "NAME": "Jan Kowalski",
                         "UNAVAILABLE_TIMES":
                             [[1, [10, 30], [12, 35]],
                              [2, [11, 30], [15, 16]]],

                         "AVAILABLE_TIMES": None,

                         "PREFERRED_TIMES":
                             [[[1, [10, 30], [12, 35]], 3],
                              [[3, [10, 30], [12, 35]], 6],
                              [None, 5]]}
        with pytest.raises(AssertionError):
            _ = bsl._load_lecturer(lecturer_data)

    def test__load_lecturer__incorrect_times(self, bsl):
        assert False

    def test_select_method_and_container(self, bsl):
        bs = BasicStructures()
        m, c = bsl._select_method_and_container(FolderNames.GROUPS, bs)
        assert m == bsl._load_group
        assert c == bs.groups

        m, c = bsl._select_method_and_container(FolderNames.LECTURERS, bs)
        assert m == bsl._load_lecturer
        assert c == bs.lecturers

        m, c = bsl._select_method_and_container(FolderNames.ROOMS, bs)
        assert m == bsl._load_room
        assert c == bs.rooms

        m, c = bsl._select_method_and_container(FolderNames.CLASSES, bs)
        assert m == bsl._load_classes
        assert c == bs.classes

    def test__load_structure__ok(self, bsl):
        path = get_path_to_sth_in_data_folder("classes_1.yaml")
        bs = BasicStructures()
        bsl._load_structure(bsl._load_classes, bs.classes, path)
        assert len(bs.classes) == 1
        assert bs.classes[0].id_ == 0
        assert bs.classes[0].name == "B5 - 105"

        path = get_path_to_sth_in_data_folder("Group.yaml")
        bs = BasicStructures()
        bsl._load_structure(bsl._load_group, bs.groups, path)
        assert len(bs.groups) == 1
        assert bs.groups[0].id_ == 33
        assert bs.groups[0].name == "group Name"

    def test__load_structure__incorrect_path(self, bsl):
        path = get_path_to_sth_in_data_folder("classes_1.yaml")
        bs = BasicStructures()
        with pytest.raises(Exception):
            bsl._load_structure(bsl._load_group, bs.groups, path)

    def test_load_all(self, bsl):
        def load_structure_mock(_, container: List, __):
            container.append([None])
        bsl2 = BasicStructureLoader()
        bsl2._load_structure = load_structure_mock
        path = get_path_to_sth_in_data_folder("data_to_load_all")
        structures = bsl2.load_all(path)
        assert len(structures.groups) == 2
        assert len(structures.lecturers) == 4
        assert len(structures.rooms) == 1
        assert len(structures.classes) == 3
