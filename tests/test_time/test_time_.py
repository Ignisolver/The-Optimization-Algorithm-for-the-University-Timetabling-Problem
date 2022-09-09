import pytest

from time_ import Time, TimeDelta
from utils.constans import DAYS
from utils.types_ import Day, Week


class TestTime:
    def test___post_init__ok_time(self):
        _ = Time(10, 20)
        _ = Time(11, 30)
        _ = Time(21, 22)
        _ = Time(9, 00)

    def test___post_init__incorrect_hour(self):
        with pytest.raises(AssertionError):
            _ = Time(-1, 20)
        with pytest.raises(AssertionError):
            _ = Time(24, 00)
        with pytest.raises(AssertionError):
            _ = Time(25, 20)
        with pytest.raises(AssertionError):
            _ = Time(99, 30)

    def test___post_init__incorrect_minute(self):
        with pytest.raises(AssertionError):
            _ = Time(10, 60)
        with pytest.raises(AssertionError):
            _ = Time(10, 70)
        with pytest.raises(AssertionError):
            _ = Time(10, -1)

    def test___post_init__ok_date(self):
        for day in DAYS:
            _ = Time(10, 20, day, Week(2))

        _ = Time(10, 20)

    def test___post_init__incorrect_date(self):
        with pytest.raises(RuntimeError):
            _ = Time(10, 20, 1, Week(2))

        with pytest.raises(RuntimeError):
            _ = Time(10, 20, Day.FRIDAY, 2)

        with pytest.raises(RuntimeError):
            _ = Time(10, 20, None, Week(1))

        with pytest.raises(RuntimeError):
            _ = Time(10, 20, Day.FRIDAY, None)

    def test_int(self):
        h1 = Time(10, 22)
        assert int(h1) == 10 * 60 + 22
        h2 = Time(0, 11)
        assert int(h2) == 11
        h3 = Time(11, 0)
        assert int(h3) == 11 * 60

    def test_add(self):
        assert Time(10, 22) + TimeDelta(-2, 5) == Time(8, 27)
        assert Time(10, 22) + TimeDelta(2, 55) == Time(13, 17)
        assert Time(10, 22) + TimeDelta(0, 50) == Time(11, 12)

    def test_sub_time(self):
        h1 = Time(10, 22)
        h2 = Time(13, 33)
        assert h2 - h1 == - (h1 - h2)
        assert h2 - h1 == TimeDelta(minutes=120 + 38 + 33)

        h1 = Time(10, 22)
        h2 = Time(13, 33, day=Day.WEDNESDAY, week=Week(3))
        assert h2 - h1 == TimeDelta(minutes=120 + 38 + 33)

        h2 = Time(10, 22)
        h1 = Time(13, 33, day=Day.WEDNESDAY, week=Week(3))
        assert h2 - h1 == - TimeDelta(minutes=120 + 38 + 33)

    def test_sub_time__incorrect_days(self):
        h1 = Time(13, 33, day=Day.WEDNESDAY, week=Week(3))
        h2 = Time(13, 33, day=Day.FRIDAY, week=Week(3))
        with pytest.raises(RuntimeError):
            _ = h2 - h1
        with pytest.raises(RuntimeError):
            _ = h1 - h2

        h1 = Time(13, 33, day=Day.WEDNESDAY, week=Week(3))
        h2 = Time(13, 33, day=Day.FRIDAY, week=Week(2))
        with pytest.raises(RuntimeError):
            _ = h2 - h1
        with pytest.raises(RuntimeError):
            _ = h1 - h2

    def test_sub_time_delta(self):
        assert Time(10, 22) - TimeDelta(-2, 5) == Time(12, 17)
        assert Time(10, 22) - TimeDelta(2, 55) == Time(7, 27)

    def test_eq__ok(self):
        assert Time(2, 5) == Time(2, 5)
        assert Time(5, 2) == Time(5, 2)
        assert Time(2, 5) != Time(2, 7)
        assert Time(2, 5) != Time(7, 5)

        assert Time(2, 5) == Time(2, 5,day=Day.WEDNESDAY, week=Week(3))
        assert Time(5, 2) == Time(5, 2,day=Day.WEDNESDAY, week=Week(3))
        assert Time(2, 5) != Time(2, 7,day=Day.WEDNESDAY, week=Week(3))
        assert Time(2, 5) != Time(7, 5,day=Day.WEDNESDAY, week=Week(3))

    def test_eq__incorrect_date(self):
        with pytest.raises(RuntimeError):
            assert Time(2, 5,day=Day.WEDNESDAY, week=Week(3)) == Time(2, 5,day=Day.WEDNESDAY, week=Week(2))
        with pytest.raises(RuntimeError):
            assert Time(5, 2,day=Day.WEDNESDAY, week=Week(3)) == Time(5, 2,day=Day.MONDAY, week=Week(3))

    def test_lt(self):
        assert Time(2, 6) > Time(2, 5)
        assert Time(3, 5) > Time(2, 5)
        assert Time(2, 5) < Time(2, 6, day=Day.WEDNESDAY, week=Week(3))
        assert Time(2, 5) < Time(3, 5, day=Day.WEDNESDAY, week=Week(3))

    def test_lt_incorrect_date(self):
        with pytest.raises(RuntimeError):
            assert Time(2, 6, day=Day.WEDNESDAY, week=Week(4)) > Time(2, 5, day=Day.WEDNESDAY, week=Week(3))
        with pytest.raises(RuntimeError):
            assert Time(3, 5, day=Day.WEDNESDAY, week=Week(3)) > Time(2, 5, day=Day.MONDAY, week=Week(3))

    def test_le(self):
        assert Time(2, 6) >= Time(2, 5)
        assert Time(3, 5) >= Time(2, 5)
        assert Time(2, 5) <= Time(2, 6)
        assert Time(2, 5) <= Time(3, 5, day=Day.WEDNESDAY, week=Week(3))
        assert Time(2, 5) >= Time(2, 5, day=Day.WEDNESDAY, week=Week(3))
        assert Time(2, 5) <= Time(2, 5, day=Day.WEDNESDAY, week=Week(3))

    def test_le__incorrect_date(self):
        with pytest.raises(RuntimeError):
            assert Time(2, 5, day=Day.TUESDAY, week=Week(3)) <= Time(3, 5, day=Day.WEDNESDAY, week=Week(3))
        with pytest.raises(RuntimeError):
            assert Time(2, 5, day=Day.WEDNESDAY, week=Week(2)) >= Time(2, 5, day=Day.WEDNESDAY, week=Week(3))
