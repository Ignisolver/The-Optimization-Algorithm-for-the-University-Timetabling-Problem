import pytest

from basic_structures.lecturer import Lecturer
from basic_structures.classes import Classes


@pytest.fixture(scope="function")
def lecturer() -> Lecturer:
    return Lecturer(1)


@pytest.fixture(scope="function")
def classes() -> Classes:
    return Classes(1, None, None, None, None, None)


class TestLecturer:
    def test__classes_is_available__ok(self, lecturer, classes):
        lecturer._available_classes.append(classes.id_)
        assert lecturer._classes_is_available(classes)
    
    def test__classes_is_available__wrong(self, lecturer, classes):
        lecturer._available_classes.append(2)
        assert lecturer._classes_is_available(classes) is False

    def test__assert_classes_available__ok(self, lecturer, classes):
        lecturer._available_classes.append(classes.id_)
        lecturer._assert_classes_available(classes)
        
    def test__assert_classes_available__wrong(self, lecturer, classes):
        lecturer._available_classes.append(2)
        with pytest.raises(RuntimeError):
            lecturer._assert_classes_available(classes)

    def test__assert_new_classes__ok(self, lecturer, classes):
        lecturer._available_classes.append(2)
        lecturer._assert_new_classes(classes)

    def test__assert_new_classes__wrong(self, lecturer, classes):
        lecturer._available_classes.append(classes.id_)
        with pytest.raises(RuntimeError):
            lecturer._assert_new_classes(classes)

    def test_add_available_classes__ok(self, lecturer, classes):
        assert lecturer._available_classes == list()
        lecturer.add_available_classes(classes)
        assert classes.id_ in lecturer._available_classes

    def test_add_available_classes__add_the_same_classes_again(self, lecturer, classes):
        assert lecturer._available_classes == list()
        lecturer.add_available_classes(classes)
        with pytest.raises(RuntimeError):
            lecturer.add_available_classes(classes)



