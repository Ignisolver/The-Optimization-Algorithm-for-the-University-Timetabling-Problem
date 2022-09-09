from dataclasses import dataclass
from typing import Union

import pytest

from time_ import Time
from time_ import TimeDelta
from time_.time_range.time_range_utils import TimeRangeInitializer
from utils.types_ import Day, Week

# todo fix tests and do them for static methods

@dataclass
class TRMock:
    start: Union[None, "Time"] = None
    end: Union["Time", None] = None
    dur: Union[TimeDelta, None] = None
    day: Union[Day, None] = None
    week: Union[Week, None] = None


@pytest.fixture
def tri() -> TimeRangeInitializer:
    return TimeRangeInitializer()


class TestTimeRangeInitializer:
    def test__is_only_start_given__ok(self, tri):
        trm = TRMock(start=Time(10, 20), dur=TimeDelta(2, 10))
        assert tri._is_only_start_given()

    def test__is_only_start_given__not(self, tri):
        trm = TRMock(start=Time(10, 20), dur=TimeDelta(2, 10), end=Time(2, 10))
        assert tri._is_only_start_given() is False

        trm = TRMock(dur=TimeDelta(2, 10), end=Time(2, 10))
        assert tri._is_only_start_given() is False

    def test__is_only_end_given__ok(self, tri):
        trm = TRMock(end=Time(10, 20), dur=TimeDelta(2, 10))
        assert tri._is_only_end_given()

    def test__is_only_end_given__not(self, tri):
        trm = TRMock(start=Time(10, 20), dur=TimeDelta(2, 10), end=Time(2, 10))
        assert tri._is_only_end_given() is False

        trm = TRMock(dur=TimeDelta(2, 10), start=Time(2, 10))
        assert tri._is_only_end_given() is False

    def test__is_duration_given__ok(self, tri):
        trm = TRMock(dur=TimeDelta(2, 10), start=Time(2, 10))
        assert tri._is_duration_given()
        trm = TRMock(dur=TimeDelta(2, 10), end=Time(2, 10))
        assert tri._is_duration_given()

    def test__is_duration_given__not(self, tri):
        trm = TRMock(end=Time(2, 10), start=Time(2, 10))
        assert tri._is_duration_given() is False

    def test__are_both_start_and_end_given__ok(self, tri):
        trm = TRMock(end=Time(2, 10), start=Time(2, 10))
        assert tri._are_both_start_and_end_given()

    def test__are_both_start_and_end_given__not(self, tri):
        trm = TRMock(dur=TimeDelta(2, 10), start=Time(2, 10))
        assert tri._are_both_start_and_end_given() is False

        trm = TRMock(dur=TimeDelta(2, 10), end=Time(2, 10))
        assert tri._are_both_start_and_end_given() is False

    def test__assert_2_of__start_end_dur__not_none__ok(self, tri):
        trm = TRMock(dur=TimeDelta(2, 10), end=Time(2, 10))
        tri._assert_2_of__start_end_dur__not_none()
        trm = TRMock(dur=TimeDelta(2, 10), start=Time(2, 10))
        tri._assert_2_of__start_end_dur__not_none()
        trm = TRMock(start=Time(2, 10), end=Time(2, 20))
        tri._assert_2_of__start_end_dur__not_none()

    def test__assert_2_of__start_end_dur__not_none__not(self, tri):
        trm = TRMock(end=Time(2, 10))
        with pytest.raises(ValueError):
            tri._assert_2_of__start_end_dur__not_none()
        trm = TRMock(dur=TimeDelta(2, 10))
        with pytest.raises(ValueError):
            tri._assert_2_of__start_end_dur__not_none()
        trm = TRMock(start=Time(2, 10))
        with pytest.raises(ValueError):
            tri._assert_2_of__start_end_dur__not_none()

    def test_assert_start_is_less_then_end__ok(self, tri):
        tri.assert_start_is_less_then_end(Time(2, 10), Time(2, 20))
        tri.assert_start_is_less_then_end(Time(2, 10), Time(3, 10))
        tri.assert_start_is_less_then_end(Time(2, 10), Time(3, 30))

    def test_assert_start_is_less_then_end__incorrect(self, tri):
        with pytest.raises(RuntimeError):
            tri.assert_start_is_less_then_end(Time(2, 10), Time(2, 10))

        with pytest.raises(RuntimeError):
            tri.assert_start_is_less_then_end(Time(2, 10), Time(1, 10))

        with pytest.raises(RuntimeError):
            tri.assert_start_is_less_then_end(Time(2, 10), Time(2, 9))

        with pytest.raises(RuntimeError):
            tri.assert_start_is_less_then_end(Time(2, 10), Time(1, 5))

    def test__assert__start_dur_end__correct__ok(self, tri):
        trm = TRMock(start=Time(2, 10), end=Time(3, 10), dur=TimeDelta(1, 0))
        tri._assert__start_dur_end__correct()
        trm = TRMock(start=Time(1, 40), end=Time(14, 2), dur=TimeDelta(12, 22))
        tri._assert__start_dur_end__correct()

    def test__assert__start_dur_end__correct__incorrect(self, tri):
        trm = TRMock(start=Time(1, 10), end=Time(3, 10), dur=TimeDelta(1, 0))
        with pytest.raises(ValueError):
            tri._assert__start_dur_end__correct()

        trm = TRMock(start=Time(2, 10), end=Time(4, 10), dur=TimeDelta(1, 0))
        with pytest.raises(ValueError):
            tri._assert__start_dur_end__correct()

        trm = TRMock(start=Time(2, 10), end=Time(3, 10), dur=TimeDelta(9, 0))
        with pytest.raises(ValueError):
            tri._assert__start_dur_end__correct()

    def test__calc_start(self, tri):
        trm = TRMock(end=Time(3, 20),
                     dur=TimeDelta(1, 10))
        tri._calc_start()
        assert tri._init_start == Time(2, 10)

        trm = TRMock(end=Time(13, 20),
                     dur=TimeDelta(1, 30))
        tri._calc_start()
        assert tri._init_start == Time(11, 50)

    def test__calc_end(self, tri):
        trm = TRMock(start=Time(12, 20),
                     dur=TimeDelta(1, 10))
        tri._calc_end()
        assert tri._init_end == Time(13, 30)

        trm = TRMock(start=Time(15, 20),
                     dur=TimeDelta(2, 45))
        tri._calc_end()
        assert tri._init_end == Time(18, 5)

    def test__calc_dur(self, tri):
        trm = TRMock(start=Time(12, 20),
                     end=Time(13, 33))
        tri._calc_end()
        assert tri._init_dur == TimeDelta(1, 13)

        trm = TRMock(start=Time(15, 20),
                     end=Time(13, 33))
        tri._calc_end()
        assert tri._init_end == Time(18, 5)

    def test__calc_start_or_end(self, tri):
        trm = TRMock(start=Time(12, 20),
                     dur=TimeDelta(1, 10))
        tri._calc_start_or_end()
        assert tri._init_end == Time(13, 30)

        trm = TRMock(end=Time(15, 20),
                     dur=TimeDelta(2, 45))
        tri._calc_start_or_end()
        assert tri._init_start == Time(12, 35)

    def test_calc_start_dur_end__ok(self, tri):
        trm = TRMock(start=Time(12, 35),
                     end=Time(15, 20),
                     dur=TimeDelta(2, 45))
        assert tri.initialize__calc_start_dur_end() == (Time(12, 35), TimeDelta(2, 45), Time(15, 20))

        trm = TRMock(start=Time(12, 35),
                     dur=TimeDelta(2, 45))
        assert tri.initialize__calc_start_dur_end() == (Time(12, 35), TimeDelta(2, 45), Time(15, 20))

        trm = TRMock(end=Time(15, 20),
                     dur=TimeDelta(2, 45))
        assert tri.initialize__calc_start_dur_end() == (Time(12, 35), TimeDelta(2, 45), Time(15, 20))

        trm = TRMock(start=Time(12, 35),
                     end=Time(15, 20))
        assert tri.initialize__calc_start_dur_end() == (Time(12, 35), TimeDelta(2, 45), Time(15, 20))

    def test_calc_start_dur_end__incorrect(self, tri):
        assert False