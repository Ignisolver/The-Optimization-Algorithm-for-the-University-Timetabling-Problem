import pytest

from time_.time_ import Time
from time_.time_range import TimeRange
from time_ import TimeDelta


class TestTimeRange:
    def test_init__ok_start_dur(self):
        tr = TimeRange(Time(10,00), TimeDelta(1,20))
        assert tr.start == Time(10, 00)
        assert tr.end == Time(11, 20)
        assert tr.dur == TimeDelta(1, 20)

    def test_init__ok_start_end(self):
        tr = TimeRange(Time(10,00), end=Time(12,20))
        assert tr.start == Time(10, 00)
        assert tr.end == Time(12, 20)
        assert tr.dur == TimeDelta(2, 20)

    def test_init__ok_dur_end(self):
        tr = TimeRange(dur=TimeDelta(3, 10), end=Time(12, 20))
        assert tr.start == Time(9, 10)
        assert tr.end == Time(12, 20)
        assert tr.dur == TimeDelta(3, 10)

    def test_init__ok_all(self):
        tr = TimeRange(start=Time(9, 10),
                       dur=TimeDelta(3, 10),
                       end=Time(12, 20))
        assert tr.start == Time(9, 10)
        assert tr.end == Time(12, 20)
        assert tr.dur == TimeDelta(3, 10)

    def test_init__all_none(self):
        with pytest.raises(ValueError):
            TimeRange()

    def test_init__only_dur(self):
        with pytest.raises(ValueError):
            TimeRange(dur=TimeDelta(2, 30))

    def test_init__incorrect(self):
        with pytest.raises(ValueError):
            TimeRange(start=Time(17,10), dur=TimeDelta(2, 30), end=Time(18,00))

    def test_init__end_less_then_sta(self):
        with pytest.raises(ValueError):
            TimeRange(start=Time(17, 10), end=Time(16, 00))


