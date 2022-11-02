import pytest

from time_ import TimeRange, Time, TimeDelta
from utils.types_ import Day, FRIDAY


class TestTimeRange:
    def test___init__ok(self):
        tr = TimeRange(Time(10, 20), Time(10, 40), TimeDelta(0, 20), FRIDAY)
        assert tr.start == Time(10, 20)
        assert tr.end == Time(10, 40)
        assert tr.dur == TimeDelta(0, 20)
        assert tr.day == FRIDAY

    def test___init__incorrect(self):
        with pytest.raises(ValueError):
            _ = TimeRange(Time(10, 20))

    def test_increase_end_ok(self):
        tr = TimeRange(Time(10, 20), Time(10, 40))
        tr.increase_end(TimeDelta(2, 10))
        assert tr.start == Time(10, 20)
        assert tr.end == Time(12, 50)
        assert tr.dur == TimeDelta(2, 30)

        tr = TimeRange(Time(10, 20), Time(11, 50))
        tr.increase_end(TimeDelta(-1, -10))
        assert tr.start == Time(10, 20)
        assert tr.end == Time(10, 40)
        assert tr.dur == TimeDelta(0, 20)

    def test_increase_end__wrong(self):
        tr = TimeRange(Time(10, 20), Time(10, 40))
        with pytest.raises(ValueError):
            tr.increase_end(TimeDelta(-1, -20))

    def test_decrease_start__ok(self):
        tr = TimeRange(Time(7, 20), Time(10, 40))
        tr.decrease_start(TimeDelta(2, 10))
        assert tr.start == Time(5, 10)
        assert tr.end == Time(10, 40)
        assert tr.dur == TimeDelta(5, 30)

        tr = TimeRange(Time(10, 20), Time(11, 50))
        tr.decrease_start(TimeDelta(-1, -10))
        assert tr.start == Time(11, 30)
        assert tr.end == Time(11, 50)
        assert tr.dur == TimeDelta(0, 20)

    def test_decrease_start__wrong(self):
        tr = TimeRange(Time(10, 20), Time(11, 50))
        with pytest.raises(ValueError):
            tr.decrease_start(TimeDelta(-6, -10))

    def test_expand_start_and_end__ok(self):
        tr = TimeRange(Time(10, 20), Time(11, 50))
        tr.expand_start_and_end(TimeDelta(2, 20))
        assert tr.start == Time(8, 00)
        assert tr.end == Time(14, 10)
        assert tr.dur == TimeDelta(6, 10)

        tr = TimeRange(Time(8, 20), Time(11, 50))
        tr.expand_start_and_end(TimeDelta(-1, -10))
        assert tr.start == Time(9, 30)
        assert tr.end == Time(10, 40)
        assert tr.dur == TimeDelta(0, 70)

    def test_expand_start_and_end__wrong(self):
        tr = TimeRange(Time(10, 20), Time(11, 50))
        with pytest.raises(AssertionError):
            tr.expand_start_and_end(TimeDelta(16, 20))

        tr = TimeRange(Time(10, 20), Time(11, 50))
        with pytest.raises(ValueError):
            tr.expand_start_and_end(TimeDelta(-4, 20))

    def test_intersect(self):
        tr1 = TimeRange(Time(8, 20), Time(11, 50))
        tr2 = TimeRange(Time(7, 20), Time(9, 50))
        assert tr1.intersect(tr2)
        assert tr2.intersect(tr1)
        t1 = Time(10, 6)
        assert tr1.intersect(t1)
        assert tr1.intersect(tr1)

    def test_to_data_generation_str(self):
        tr1 = TimeRange(Time(8, 20), Time(11, 50), day=Day(2))
        assert tr1.to_generate() == [3, [8, 20], [11, 50]]
