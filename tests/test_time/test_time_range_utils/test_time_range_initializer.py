from dataclasses import dataclass
from typing import Union

import pytest

from time_ import Time
from time_ import TimeDelta
from time_.time_range.time_range_utils import TimeRangeInitializer
from utils.types_ import Day, Week


@dataclass
class TRMock:
    start: Union[None, "Time"] = None
    end: Union["Time", None] = None
    dur: Union[TimeDelta, None] = None
    day: Union[Day, None] = None


@pytest.fixture
def tri() -> TimeRangeInitializer:
    return TimeRangeInitializer()


class TestTimeRangeInitializer:
    def test__assert_2_of__start_end_dur__not_none__ok(self, tri):
        tri._assert_2_of__start_end_dur__not_none(Time(10, 10), TimeDelta(12, 30), None)
        tri._assert_2_of__start_end_dur__not_none(None, TimeDelta(12, 30), Time(13, 10))
        tri._assert_2_of__start_end_dur__not_none(Time(10, 10), None, Time(12, 10))

    def test__assert_2_of__start_end_dur__not_none__not(self, tri):
        with pytest.raises(ValueError):
            tri._assert_2_of__start_end_dur__not_none(Time(10, 10), None, None)
        with pytest.raises(ValueError):
            tri._assert_2_of__start_end_dur__not_none(None, TimeDelta(12, 30), None)
        with pytest.raises(ValueError):
            tri._assert_2_of__start_end_dur__not_none(None, None, Time(12, 10))
        with pytest.raises(ValueError):
            tri._assert_2_of__start_end_dur__not_none(None, None, None)

    def test__assert__start_dur_end__correct__ok(self, tri):
        tri.assert__start_dur_end__correct(start=Time(2, 10), end=Time(3, 10), dur=TimeDelta(1, 0))
        tri.assert__start_dur_end__correct(start=Time(1, 40), end=Time(14, 2), dur=TimeDelta(12, 22))

    def test_assert__start_dur_end__correct__incorrect(self, tri):
        with pytest.raises(ValueError):
            tri.assert__start_dur_end__correct(start=Time(1, 10), end=Time(3, 10), dur=TimeDelta(1, 0))

        with pytest.raises(ValueError):
            tri.assert__start_dur_end__correct(start=Time(2, 10), end=Time(4, 10), dur=TimeDelta(1, 0))

        with pytest.raises(ValueError):
            tri.assert__start_dur_end__correct(start=Time(2, 10), end=Time(3, 10), dur=TimeDelta(9, 0))

    def test__calc_start(self, tri):
        assert tri._calc_start(end=Time(3, 20), dur=TimeDelta(1, 10)) == Time(2, 10)
        assert tri._calc_start(end=Time(13, 20), dur=TimeDelta(1, 30)) == Time(11, 50)

    def test__calc_end(self, tri):
        assert tri._calc_end(start=Time(12, 20), dur=TimeDelta(1, 10)) == Time(13, 30)

        assert tri._calc_end(start=Time(15, 20), dur=TimeDelta(2, 45)) == Time(18, 5)

    def test__calc_dur(self, tri):
        assert tri._calc_dur(start=Time(12, 20), end=Time(13, 33)) == TimeDelta(1, 13)
        assert tri._calc_dur(start=Time(10, 20), end=Time(13, 33)) == TimeDelta(3, 13)

    def test_calc_start_dur_end__ok(self, tri):
        assert tri.calc_start_dur_end(start=Time(12, 35),
                                      end=Time(15, 20),
                                      dur=TimeDelta(2, 45)) == (Time(12, 35), TimeDelta(2, 45), Time(15, 20))

        assert tri.calc_start_dur_end(start=Time(12, 35),
                                      dur=TimeDelta(2, 45)) == (Time(12, 35), TimeDelta(2, 45), Time(15, 20))

        assert tri.calc_start_dur_end(end=Time(15, 20),
                                      dur=TimeDelta(2, 45)) == (Time(12, 35), TimeDelta(2, 45), Time(15, 20))

        assert tri.calc_start_dur_end(start=Time(12, 35),
                                      end=Time(15, 20)) == (Time(12, 35), TimeDelta(2, 45), Time(15, 20))

    def test_calc_start_dur_end__incorrect(self, tri):
        with pytest.raises(ValueError):
            assert tri.calc_start_dur_end(start=Time(12, 35), end=Time(12, 20))

        with pytest.raises(ValueError):
            assert tri.calc_start_dur_end(start=Time(12, 35), end=Time(13, 20), dur=TimeDelta(2, 15))

        with pytest.raises(ValueError):
            assert tri.calc_start_dur_end(start=Time(12, 35))