from utils.none_machine import NM


class TestNoneMachine:
    def test_both_nones(self):
        assert NM.both_nones(None, None) is True
        assert NM.both_nones(1, None) is False
        assert NM.both_nones(None, 1) is False
        assert NM.both_nones(1, 1) is False

    def test_both_not_none(self):
        assert NM.both_not_none(None, None) is False
        assert NM.both_not_none(1, None) is False
        assert NM.both_not_none(None, 1) is False
        assert NM.both_not_none(1, 1) is True

    def test_count_nones(self):
        assert NM.count_nones((1,2,3, None, None)) == 2
        assert NM.count_nones((None,)) == 1
        assert NM.count_nones((1, None)) == 1
        assert NM.count_nones((1, 2)) == 0

    def test_contain_one_none(self):
        assert NM.contain_one_none((1,2,3,4, None)) is True
        assert NM.contain_one_none((None,)) is True
        assert NM.contain_one_none((1,2,3,None,None)) is False
        assert NM.contain_one_none((1,2,3)) is False

    def test_is_nones_amount(self):
        assert NM.is_nones_amount((1,2,3,4, None), 1)
        assert NM.is_nones_amount((1,None, 2,3,4, None, None), 3)
        assert NM.is_nones_amount((1,2,3,4), 0)
