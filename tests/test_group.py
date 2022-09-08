import pytest

from basic_structures.classes import Classes
from basic_structures.group import Group


@pytest.fixture
def group() -> Group:
    return Group(1, 30)


classes_1 = Classes(1, None, None, None, None, None)
classes_2 = Classes(2, None, None, None, None, None)
classes_3 = Classes(3, None, None, None, None, None)


class TestGroup:
    def test__is_classes_assigned__ok(self, group):
        group._assigned_classes[classes_1.id_] = classes_1
        assert group._is_classes_in_assigned(classes_1)

    def test__is_classes_assigned__wrong(self, group):
        group._assigned_classes[classes_1.id_] = classes_1
        assert group._is_classes_in_assigned(classes_2) is False
        
    def test__is_classes_available__ok(self, group):
        group._unassigned_classes[classes_1.id_] = classes_1
        assert group._is_classes_in_available_unassigned(classes_1)

    def test__is_classes_available__wrong(self, group):
        group._unassigned_classes[classes_1.id_] = classes_1
        assert group._is_classes_in_available_unassigned(classes_2) is False

    def test__assert_classes_available__ok(self, group):
        group._unassigned_classes[classes_1.id_] = classes_1
        group._assert_classes_in_available_unassigned(classes_1)

    def test__assert_classes_available__wrong(self, group):
        group._unassigned_classes[classes_1.id_] = classes_1
        with pytest.raises(RuntimeError):
            group._assert_classes_in_available_unassigned(classes_2)

    def test__assert_classes_not_added_yet__ok(self, group):
        group._unassigned_classes[classes_1.id_] = classes_1
        group._assert_classes_not_in_available_unassigned(classes_2)

    def test__assert_classes_not_added_yet__wrong(self, group):
        group._unassigned_classes[classes_1.id_] = classes_1
        with pytest.raises(RuntimeError):
            group._assert_classes_not_in_available_unassigned(classes_1)

    def test__assert_classes_assigned__ok(self, group):
        group._assigned_classes[classes_1.id_] = classes_1
        group._assert_classes_in_assigned(classes_1)

    def test__assert_classes_assigned__wrong(self, group):
        group._assigned_classes[classes_1.id_] = classes_1
        with pytest.raises(RuntimeError):
            group._assert_classes_in_available_unassigned(classes_2)

    def test__move_classes_to_assigned__ok(self, group):
        group._unassigned_classes[classes_1.id_] = classes_1
        group._move_classes_to_assigned(classes_1)
        assert group._assigned_classes[classes_1.id_] == classes_1

    def test__move_classes_to_assigned__not_in_unassigned(self, group):
        group._unassigned_classes[classes_2.id_] = classes_2
        with pytest.raises(KeyError):
            group._move_classes_to_assigned(classes_1)

    def test__move_classes_to_unassigned__ok(self, group):
        group._assigned_classes[classes_1.id_] = classes_1
        group._move_classes_to_unassigned(classes_1)
        assert group._unassigned_classes[classes_1.id_] == classes_1

    def test__move_classes_to_unassigned__not_in_assigned(self, group):
        group._assigned_classes[classes_2.id_] = classes_2
        with pytest.raises(KeyError):
            group._move_classes_to_unassigned(classes_1)
        
    def test_add_classes_to_assign__ok(self, group):
        group.add_classes_to_assign(classes_1)
        assert group._unassigned_classes[classes_1.id_] == classes_1

    def test_add_classes_to_assign__already_added(self, group):
        group.add_classes_to_assign(classes_1)
        with pytest.raises(RuntimeError):
            group.unassign(classes_1)

    def test_assign__not_in_unassigned(self, group):
        group.add_classes_to_assign(classes_2)
        with pytest.raises(RuntimeError):
            group.assign(classes_1)

    def test_assign__already_in_assigned(self, group):
        group._assigned_classes[classes_1.id_] = classes_1
        with pytest.raises(RuntimeError):
            group.assign(classes_1)

    def test_unassign__not_in_assigned(self, group):
        with pytest.raises(RuntimeError):
            group.unassign(classes_2)

    def test_assign__already_in_unassigned(self, group):
        group.add_classes_to_assign(classes_1)
        group._unassigned_classes[classes_1.id_] = classes_1
        with pytest.raises(RuntimeError):
            group.unassign(classes_1)

    def test___add_already_assigned(self, group):
        group.add_classes_to_assign(classes_1)
        group.assign(classes_1)
        with pytest.raises(RuntimeError):
            group.add_classes_to_assign(classes_1)

    def test___assign_already_assigned(self, group):
        group.add_classes_to_assign(classes_1)
        group.assign(classes_1)
        with pytest.raises(RuntimeError):
            group.assign(classes_1)

