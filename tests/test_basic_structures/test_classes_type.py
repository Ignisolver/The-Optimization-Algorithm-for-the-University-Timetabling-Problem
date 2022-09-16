import pytest

from utils.types_ import ClassesType, ClassesTypes


def test_classes_type__ok():
    c = ClassesType("W-N-1")
    assert c.el_no == ClassesTypes.NORMAL
    assert c.lect_lab == ClassesTypes.LECTURE
    assert c.weeks == 1

    c = ClassesType("L-E-4")
    assert c.el_no == ClassesTypes.ELECTIVE
    assert c.lect_lab == ClassesTypes.LABORATORY
    assert c.weeks == 4


def test_classes_type__incorrect():
    with pytest.raises(ValueError):
        _ = ClassesType("WN-1")

    with pytest.raises(ValueError):
        _ = ClassesType("W-C-1")

    with pytest.raises(ValueError):
        _ = ClassesType("W-E-0")

