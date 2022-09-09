import pytest

from time_ import Time, TimeRange
from time_.time_utils import DateCorrectnessCaretaker
from utils.constans import DAYS
from utils.types_ import Day, Week


@pytest.fixture
def tdcc() -> DateCorrectnessCaretaker:
    return DateCorrectnessCaretaker()


class TestDateCorrectnessCaretaker:
    def test__are_weeks_and_days_same(self, tdcc):
        t1 = Time(10, 20, Day.MONDAY, Week(1))
        t2 = Time(10, 20, Day.MONDAY, Week(1))
        assert tdcc._are_weeks_and_days_same(t1, t2) is True
        t1 = Time(10, 20, Day.MONDAY, Week(1))
        t2 = Time(10, 20, Day.TUESDAY, Week(1))
        assert tdcc._are_weeks_and_days_same(t1, t2) is False
        t1 = Time(10, 20, Day.MONDAY, Week(1))
        t2 = Time(10, 20, Day.MONDAY, Week(2))
        assert tdcc._are_weeks_and_days_same(t1, t2) is False

    def test__are_both_day_and_week_in_self_or_other_nones(self, tdcc):
        t1 = Time(10, 20, None, None)
        t2 = Time(11, 20, Day.MONDAY, Week(1))
        assert tdcc._are_both_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, Day.MONDAY, Week(1))
        t2 = Time(11, 20, None, None)
        assert tdcc._are_both_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, None, None)
        t2 = Time(11, 20, None, None)
        assert tdcc._are_both_day_and_week_in_self_or_other_nones(t1, t2) is True
        t1 = Time(10, 20, Day.MONDAY, Week(1))
        t2 = Time(11, 20, Day.MONDAY, Week(1))
        assert tdcc._are_both_day_and_week_in_self_or_other_nones(t1, t2) is False

        t1 = TimeRange(start=Time(10, 20), end=Time(12, 50), day = None,week= None)
        t2 = TimeRange(start=Time(11, 20), end=Time(12, 50), day = Day.MONDAY, week=Week(1))
        assert tdcc._are_both_day_and_week_in_self_or_other_nones(t1, t2) is True
        
        t1 = TimeRange(start=Time(10, 20), end=Time(12, 50), day = Day.MONDAY,week= Week(1))
        t2 = TimeRange(start=Time(11, 20), end=Time(12, 50), day = None,week= None)
        assert tdcc._are_both_day_and_week_in_self_or_other_nones(t1, t2) is True
        
        t1 = TimeRange(start=Time(10, 20), end=Time(12, 50), day = None,week= None)
        t2 = TimeRange(start=Time(11, 20), end=Time(12, 50), day = None, week=None)
        assert tdcc._are_both_day_and_week_in_self_or_other_nones(t1, t2) is True
        
        t1 = TimeRange(start=Time(10, 20), end=Time(12, 50), day = Day.MONDAY,week= Week(1))
        t2 = TimeRange(start=Time(11, 20), end=Time(12, 50), day = Day.MONDAY,week= Week(1))
        assert tdcc._are_both_day_and_week_in_self_or_other_nones(t1, t2) is False

    def test_assert_initial_arguments_day_and_week_correct__ok(self, tdcc):
        tdcc.assert_initial_arguments_day_and_week_correct(None, None)
        for day in DAYS:
            tdcc.assert_initial_arguments_day_and_week_correct(day, Week(1))

    def test_assert_days_and_weeks_correctness__incorrect_type(self, tdcc):
        with pytest.raises(RuntimeError):
            tdcc.assert_initial_arguments_day_and_week_correct(1, Week(1))
        with pytest.raises(RuntimeError):
            tdcc.assert_initial_arguments_day_and_week_correct(Day.MONDAY, 1)
        with pytest.raises(RuntimeError):
            tdcc.assert_initial_arguments_day_and_week_correct(2, 1)

    def test_assert_days_and_weeks_correctness__incorrect__not_both_set_or_none(self, tdcc):
        with pytest.raises(RuntimeError):
            tdcc.assert_initial_arguments_day_and_week_correct(None, Week(1))
        with pytest.raises(RuntimeError):
            tdcc.assert_initial_arguments_day_and_week_correct(Day.MONDAY, None)

    def test__are_day_and_week_nones(self, tdcc):
        assert tdcc._are_day_and_week_nones(None, None) is True
        assert tdcc._are_day_and_week_nones(Day.SUNDAY, None) is False
        assert tdcc._are_day_and_week_nones(None, Week(2)) is False
        assert tdcc._are_day_and_week_nones(Day.SUNDAY, Week(2)) is False

    def test__are_day_and_week_set(self, tdcc):
        assert tdcc._are_day_and_week_set(None, None) is False
        assert tdcc._are_day_and_week_set(Day.SUNDAY, None) is False
        assert tdcc._are_day_and_week_set(None, Week(2)) is False
        assert tdcc._are_day_and_week_set(Day.SUNDAY, Week(2)) is True

    def test__assert_days_and_weeks_same__ok(self, tdcc):
        tdcc._assert_days_and_weeks_same(Time(14, 30,day=Day.MONDAY,week=Week(1)),
                                         Time(20, 15,day=Day.MONDAY,week=Week(1)))

    def test__assert_days_and_weeks_same__incorrect(self, tdcc):

        with pytest.raises(RuntimeError):
            tdcc._assert_days_and_weeks_same(Time(14, 30, day=Day.TUESDAY, week=Week(1)),
                                             Time(20, 15, day=Day.TUESDAY, week=Week(2)))
        with pytest.raises(RuntimeError):
            tdcc._assert_days_and_weeks_same(Time(14, 30, day=Day.SUNDAY, week=Week(1)),
                                             Time(20, 15, day=Day.SATURDAY, week=Week(1)))
        with pytest.raises(RuntimeError):
            tdcc._assert_days_and_weeks_same(Time(14, 30, day=Day.SUNDAY, week=Week(1)),
                                             Time(20, 15, day=Day.SATURDAY, week=Week(2)))




