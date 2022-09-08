import pytest

from time_ import TimeDelta


class TestTimeDelta:
    def test__calc_total_amount_of_minutes(self):
        td = TimeDelta(1, 1)
        assert td._calc_total_amount_of_minutes(1, 10) == 70
        assert td._calc_total_amount_of_minutes(-2, 50) == -70
        assert td._calc_total_amount_of_minutes(1, -30) == 30
        assert td._calc_total_amount_of_minutes(1, -90) == -30

    def test_init_float(self):
        with pytest.raises(AssertionError):
            TimeDelta(minutes=0.3)
        with pytest.raises(AssertionError):
            TimeDelta(hours=0.3)
        assert TimeDelta(1, -2) == TimeDelta(0, 58)

    def test_init_ok(self):
        td = TimeDelta(1, 1)
        assert td.hours == 1
        assert td.minutes == 1
        td = TimeDelta(1, 65)
        assert td.hours == 2
        assert td.minutes == 5
        td = TimeDelta(1, -70)
        assert td.hours == -1
        assert td.minutes == 50

    def test_neg(self):
        assert TimeDelta(9, 2) == - TimeDelta(-9, -2)
        assert TimeDelta(-0, -3) == - TimeDelta(0, 3)
        assert TimeDelta(1, -70) == - TimeDelta(0, 10)

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
