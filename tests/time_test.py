import pytest

from time_ import Time, TimeDelta


class TestHour:
    def test_int(self):
        h1 = Time(10, 22)
        assert int(h1) == 10*60 + 22
        h2 = Time(0, 11)
        assert int(h2) == 11
        h3 = Time(11, 0)
        assert int(h3) == 11 * 60

    def test_add(self):
        assert Time(10, 22) + TimeDelta(-2, 5) == Time(8, 27)
        assert Time(10, 22) + TimeDelta(2, 55) == Time(13, 17)

    def test_sub_hour(self):
        h1 = Time(10, 22)
        h2 = Time(13, 33)
        assert h2 - h1 == - (h1 - h2)
        assert h2 - h1 == TimeDelta(minutes=120 + 38 + 33)

    def test_sub_hour_delta(self):
        assert Time(10, 22) - TimeDelta(-2, 5) == Time(12, 17)
        assert Time(10, 22) - TimeDelta(2, 55) == Time(7, 27)

    def test_eq(self):
        assert Time(2, 5) == Time(2, 5)
        assert Time(5, 2) == Time(5, 2)
        assert Time(2, 5) != Time(2, 7)
        assert Time(2, 5) != Time(7, 5)

    def test_lt(self):
        assert Time(2, 6) > Time(2, 5)
        assert Time(3, 5) > Time(2, 5)
        assert Time(2, 5) < Time(2, 6)
        assert Time(2, 5) < Time(3, 5)

    def test_le(self):
        assert Time(2, 6) >= Time(2, 5)
        assert Time(3, 5) >= Time(2, 5)
        assert Time(2, 5) <= Time(2, 6)
        assert Time(2, 5) <= Time(3, 5)
        assert Time(2, 5) >= Time(2, 5)
        assert Time(2, 5) <= Time(2, 5)



class TestHourDelta:
    def test_init(self):
        with pytest.raises(AssertionError):
            TimeDelta(minutes=0.3)
        with pytest.raises(AssertionError):
            TimeDelta(hours=0.3)
        assert TimeDelta(1, -2) == TimeDelta(0, 58)

    def test_neg(self):
        assert TimeDelta(9, 2) == - TimeDelta(-9, -2)

    def test_add(self):
        assert TimeDelta(9, 2) + TimeDelta(-9, -2) == TimeDelta(0, 0)
        assert TimeDelta(10, 200) + TimeDelta(0, -2) == TimeDelta(10, 198)
        assert TimeDelta(-5, 2) + TimeDelta(-5, 40) == TimeDelta(-10, 42)
        assert TimeDelta(0, 1) + TimeDelta(1, 0) == TimeDelta(1, 1)
        assert TimeDelta(1, 30) + TimeDelta(1, 35) == TimeDelta(3, 5)

    def test_sub(self):
        assert TimeDelta(9, 2) - TimeDelta(-9, -2) == TimeDelta(18, 4)
        assert TimeDelta(10, 200) - TimeDelta(0, -2) == TimeDelta(10, 202)
        assert TimeDelta(-5, 2) - TimeDelta(-5, 40) == TimeDelta(0, -38)
        assert TimeDelta(0, 1) - TimeDelta(1, 0) == TimeDelta(0, -59)

    def test_eq(self):
        assert TimeDelta(-9, -2) == TimeDelta(-8, -62)
        assert TimeDelta(9, -2) == TimeDelta(8, 58)
        assert TimeDelta(-9, -2) == TimeDelta(-9, -2)
        assert TimeDelta(9, 2) == TimeDelta(9, 2)

    def test_lt(self):
        assert TimeDelta(2, 6) > TimeDelta(2, 5)
        assert TimeDelta(3, 5) > TimeDelta(2, 5)
        assert TimeDelta(2, 5) < TimeDelta(2, 6)
        assert TimeDelta(2, 5) < TimeDelta(3, 5)

        assert TimeDelta(2, 6) > TimeDelta(2, -10)
        assert TimeDelta(3, 6) > TimeDelta(2, -599)
        assert TimeDelta(2, -10) < TimeDelta(2, 6)
        assert TimeDelta(-2, -5) < TimeDelta(3, 5)

    def test_le(self):
        assert TimeDelta(2, 6) >= TimeDelta(2, 5)
        assert TimeDelta(3, 5) >= TimeDelta(2, 5)
        assert TimeDelta(2, 5) <= TimeDelta(2, 6)
        assert TimeDelta(2, 5) <= TimeDelta(3, 5)
        assert TimeDelta(2, 5) >= TimeDelta(2, 5)
        assert TimeDelta(2, 5) <= TimeDelta(2, 5)

        assert TimeDelta(2, 6) >= TimeDelta(-2, 5)
        assert TimeDelta(3, 5) >= TimeDelta(-2, 5)
        assert TimeDelta(-2, 5) <= TimeDelta(2, 6)
        assert TimeDelta(-2, 5) <= TimeDelta(3, 5)
        assert TimeDelta(2, 5) >= TimeDelta(-2, 5)
        assert TimeDelta(2, -5) <= TimeDelta(2, 5)
