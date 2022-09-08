import pytest

from time_ import Time
from time_.time_utils import DateCorrectnessCaretaker
from utils.types_ import Day, Week


@pytest.fixture
def tdcc() -> DateCorrectnessCaretaker:
    return DateCorrectnessCaretaker()


class TestDateCorrectnessCaretaker:
    def test__is_weeks_and_days_same(self, tdcc):
        t1 = Time(10, 20, Day.MONDAY, Week(1))
        t2 = Time(10, 20, Day.MONDAY, Week(1))
        assert tdcc._is_weeks_and_days_same(t1, t2) is True
        t1 = Time(10, 20, Day.MONDAY, Week(1))
        t2 = Time(10, 20, Day.TUESDAY, Week(1))
        assert tdcc._is_weeks_and_days_same(t1, t2) is False
        t1 = Time(10, 20, Day.MONDAY, Week(1))
        t2 = Time(10, 20, Day.MONDAY, Week(2))
        assert tdcc._is_weeks_and_days_same(t1, t2) is False

    def test__is_day_and_week_in_self_or_other_nones(self, tdcc):
        t1 = Time(10, 20, Day.MONDAY, None)
        t2 = Time(10, 20, Day.MONDAY, Week(1))
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, None, None)
        t2 = Time(10, 20, Day.MONDAY, Week(1))
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, Day.MONDAY, None)
        t2 = Time(10, 20, Day.MONDAY, None)
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, Day.MONDAY, None)
        t2 = Time(10, 20, None, Week(1))
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, None, None)
        t2 = Time(10, 20, Day.MONDAY, None)
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, None, None)
        t2 = Time(10, 20, None, Week(1))
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, Day.MONDAY, None)
        t2 = Time(10, 20, Day.MONDAY, None)
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, None, None)
        t2 = Time(10, 20, None, None)
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, None, Week(1))
        t2 = Time(10, 20, Day.MONDAY, Week(1))
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, Day.MONDAY, Week(1))
        t2 = Time(10, 20, None, Week(1))
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, Day.MONDAY, Week(1))
        t2 = Time(10, 20, Day.MONDAY, None)
        assert tdcc._is_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, None, None)
    def test__assert_days_and_weeks_same(self):
        assert False

    def test_assert_days_and_weeks_correctness(self):
        assert False

    def test_assert_arguments_day_and_week_correct(self):
        assert False
