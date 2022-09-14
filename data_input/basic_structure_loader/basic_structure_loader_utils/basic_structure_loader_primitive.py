from typing import Tuple

from data_input.basic_structure_loader.basic_structure_loader_utils.input_types import InputStructureType, Tag


class BasicStructureLoaderPrimitive:
    @staticmethod
    def _assert_type(type_to_check: InputStructureType, correct_type: InputStructureType):
        assert type_to_check == correct_type

    @staticmethod
    def _assert_positive_int(value):
        assert isinstance(value, int)
        assert value >= 0

    @staticmethod
    def _assert_name_correct(name):
        assert isinstance(name, str)

    def _assert_correct_ids_tuple(self, tuple_):
        id_set = set()
        for id_ in tuple_:
            self._assert_positive_int(id_)
            id_set.add(id_)
        assert len(id_set) == len(tuple_)

    def _load_id_and_name(self, data: dict, correct_type) -> Tuple[int, str]:
        type_ = InputStructureType(data[Tag.TYPE])
        self._assert_type(type_, correct_type)

        id_ = data[Tag.ID]
        self._assert_positive_int(id_)

        name = data[Tag.NAME]
        self._assert_name_correct(name)
        return id_, name
