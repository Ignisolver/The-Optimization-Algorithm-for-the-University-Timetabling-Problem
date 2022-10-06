import pytest

from old.data_input.basic_structure_loader.basic_structure_loader_utils.basic_structure_loader_primitive import \
    BasicStructureLoaderPrimitive
from old.data_input.basic_structure_loader.basic_structure_loader_utils.input_types import \
    InputStructureType as InpST


@pytest.fixture
def bslp() -> BasicStructureLoaderPrimitive():
    return BasicStructureLoaderPrimitive()


class TestBasicStructureLoaderPrimitive:
    def test__assert_type__ok(self, bslp):
        bslp._assert_type(InpST.Room,
                          InpST.Room)

        bslp._assert_type(InpST.Group,
                          InpST.Group)

        bslp._assert_type(InpST.Lecturer,
                          InpST.Lecturer)

        bslp._assert_type(InpST.Classes,
                          InpST.Classes)

    def test__assert_type__incorrect(self, bslp):
        with pytest.raises(AssertionError):
            bslp._assert_type(InpST.Room, InpST.Group)
        with pytest.raises(AssertionError):
            bslp._assert_type(InpST.Lecturer, InpST.Classes)

    def test__assert_positive_int__ok(self, bslp):
        bslp._assert_not_negative_int(1)
        bslp._assert_not_negative_int(0)
        bslp._assert_not_negative_int(30)

    def test__assert_not_negative_int__incorrect(self, bslp):
        with pytest.raises(AssertionError):
            bslp._assert_not_negative_int(3.4)
        with pytest.raises(AssertionError):
            bslp._assert_not_negative_int(-1)

    def test__assert_name_correct__ok(self, bslp):
        bslp._assert_name_correct("Ewa")
        bslp._assert_name_correct("573287")
        bslp._assert_name_correct("POsjs Woif")

    def test__assert_name_correct__incorrect(self, bslp):
        with pytest.raises(AssertionError):
            bslp._assert_name_correct(3)

    def test__assert_correct_ids_tuple__ok(self, bslp):
        bslp._assert_correct_ids_tuple([1, 2, 3, 4])
        bslp._assert_correct_ids_tuple([])

    def test__assert_correct_ids_tuple__empty(self, bslp):
        with pytest.raises(AssertionError):
            bslp._assert_correct_ids_tuple([], empty_able=False)

    def test__assert_correct_ids_tuple__incorrect(self, bslp):
        with pytest.raises(AssertionError):
            bslp._assert_correct_ids_tuple([-1, 1, 2, 3])
        with pytest.raises(AssertionError):
            bslp._assert_correct_ids_tuple([33, "ola", 33])
        with pytest.raises(AssertionError):
            bslp._assert_correct_ids_tuple("piiow")
        with pytest.raises(AssertionError):
            bslp._assert_correct_ids_tuple("[1,2,3,4]")
        with pytest.raises(AssertionError):
            bslp._assert_correct_ids_tuple([1, 2, 3, 4, 4, 21, 2, 2])

    def test__load_id_and_name__ok(self, bslp):
        dict_ = {"TYPE": InpST.Group,
                 "ID": 20,
                 "NAME": "koza"}
        id_, name = bslp._load_id_and_name(dict_, InpST.Group)
        assert id_ == 20
        assert name == "koza"

    def test__load_id_and_name__incorrect(self, bslp):
        dict_ = {"TYPE": InpST.Group,
                 "ID": 20,
                 "NAME": "koza"}
        with pytest.raises(AssertionError):
            bslp._load_id_and_name(dict_, InpST.Lecturer)
