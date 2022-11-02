import pytest

from time_ import TimeRange, Time
from time_.time_range.time_range_utils import TimeRangeIntersectDetector


@pytest.fixture
def trid() -> TimeRangeIntersectDetector:
    return TimeRangeIntersectDetector()


class TestTimeRangeIntersectDetector:
    def test__one_is_in_other__ok(self, trid):
        tr1 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        tr2 = TimeRange(start=Time(10, 0), end=Time(12, 00))
        assert trid._one_is_in_other(tr1, tr2) is True

        tr1 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        tr2 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        assert trid._one_is_in_other(tr1, tr2) is True

        tr1 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        tr2 = TimeRange(start=Time(10, 30), end=Time(12, 00))
        assert trid._one_is_in_other(tr1, tr2) is True

        tr1 = TimeRange(start=Time(10, 30), end=Time(12, 00))
        tr2 = TimeRange(start=Time(10, 0), end=Time(12, 00))
        assert trid._one_is_in_other(tr1, tr2) is True

    def test__other_is_in_one__ok(self, trid):
        tr1 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        tr2 = TimeRange(start=Time(10, 0), end=Time(12, 00))
        assert trid._other_is_in_one(tr2, tr1) is True

        tr1 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        tr2 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        assert trid._other_is_in_one(tr2, tr1) is True

        tr1 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        tr2 = TimeRange(start=Time(10, 30), end=Time(12, 00))
        assert trid._other_is_in_one(tr2, tr1) is True

        tr1 = TimeRange(start=Time(10, 30), end=Time(12, 00))
        tr2 = TimeRange(start=Time(10, 0), end=Time(12, 00))
        assert trid._other_is_in_one(tr2, tr1) is True

    def test__other_ends_in_one__ok(self, trid):
        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(10, 20), end=Time(14, 13))
        assert trid._other_ends_in_one(tr1, tr2) is True

        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(10, 20), end=Time(16, 13))
        assert trid._other_ends_in_one(tr1, tr2) is True

        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(10, 20), end=Time(17, 16))
        assert trid._other_ends_in_one(tr1, tr2) is True

    def test__other_starts_in_one__ok(self, trid):
        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(14, 12), end=Time(18, 20))
        assert trid._other_starts_in_one(tr1, tr2) is True

        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(16, 12), end=Time(18, 20))
        assert trid._other_starts_in_one(tr1, tr2) is True

        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(16, 19), end=Time(18, 20))
        assert trid._other_starts_in_one(tr1, tr2) is True

        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(14, 12), end=Time(18, 20))
        assert trid._other_starts_in_one(tr1, tr2) is True

    def test__is_time_in_time_range__ok(self, trid):
        t1 = Time(12, 10)
        tr2 = TimeRange(start=Time(10, 00), end=Time(13, 00))
        assert trid._is_time_in_time_range(tr2, t1) is True

        t1 = Time(10, 1)
        tr2 = TimeRange(start=Time(10, 00), end=Time(13, 00))
        assert trid._is_time_in_time_range(tr2, t1) is True

        t1 = Time(12, 59)
        tr2 = TimeRange(start=Time(10, 00), end=Time(13, 00))
        assert trid._is_time_in_time_range(tr2, t1) is True

    def test__is_time_ranges_intersect__ok(self, trid):
        tr1 = TimeRange(start=Time(10, 00), end=Time(12, 00))
        tr2 = TimeRange(start=Time(10, 00), end=Time(12, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is True

        tr1 = TimeRange(start=Time(9, 00), end=Time(12, 00))
        tr2 = TimeRange(start=Time(10, 00), end=Time(12, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is True

        tr1 = TimeRange(start=Time(10, 00), end=Time(13, 00))
        tr2 = TimeRange(start=Time(10, 00), end=Time(12, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is True

        tr1 = TimeRange(start=Time(9, 00), end=Time(13, 00))
        tr2 = TimeRange(start=Time(10, 00), end=Time(12, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is True

        tr1 = TimeRange(start=Time(10, 00), end=Time(12, 00))
        tr2 = TimeRange(start=Time(9, 00), end=Time(13, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is True

        tr1 = TimeRange(start=Time(9, 00), end=Time(11, 00))
        tr2 = TimeRange(start=Time(10, 00), end=Time(12, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is True

        tr1 = TimeRange(start=Time(11, 00), end=Time(13, 00))
        tr2 = TimeRange(start=Time(10, 00), end=Time(12, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is True

    def test_is_intersection__ok(self, trid):
        t = Time(10, 20)
        tr = TimeRange(start=Time(10, 00), end=Time(11, 00))
        assert trid.is_intersection(tr, t) is True

        tr1 = TimeRange(start=Time(9, 30), end=Time(11, 00))
        tr2 = TimeRange(start=Time(10, 00), end=Time(11, 00))
        assert trid.is_intersection(tr1, tr2) is True

    def test__one_is_in_other__not(self, trid):
        tr1 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        tr2 = TimeRange(start=Time(11, 30), end=Time(12, 00))
        assert trid._one_is_in_other(tr2, tr1) is False

        tr1 = TimeRange(start=Time(11, 30), end=Time(12, 30))
        tr2 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        assert trid._one_is_in_other(tr1, tr2) is False

        tr1 = TimeRange(start=Time(11, 30), end=Time(12, 30))
        tr2 = TimeRange(start=Time(10, 30), end=Time(12, 00))
        assert trid._one_is_in_other(tr1, tr2) is False

        tr1 = TimeRange(start=Time(10, 30), end=Time(12, 30))
        tr2 = TimeRange(start=Time(12, 0), end=Time(13, 00))
        assert trid._one_is_in_other(tr1, tr2) is False

        tr1 = TimeRange(start=Time(10, 30), end=Time(14, 30))
        tr2 = TimeRange(start=Time(12, 0), end=Time(13, 00))
        assert trid._one_is_in_other(tr1, tr2) is False

        tr1 = TimeRange(start=Time(10, 30), end=Time(12, 30))
        tr2 = TimeRange(start=Time(12, 40), end=Time(13, 00))
        assert trid._one_is_in_other(tr1, tr2) is False

        tr1 = TimeRange(start=Time(12, 40), end=Time(15, 00))
        tr2 = TimeRange(start=Time(10, 30), end=Time(12, 30))
        assert trid._one_is_in_other(tr1, tr2) is False

    def test__other_is_in_one__not(self, trid):
        tr1 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        tr2 = TimeRange(start=Time(11, 30), end=Time(12, 00))
        assert trid._one_is_in_other(tr1, tr2) is False

        tr1 = TimeRange(start=Time(11, 30), end=Time(12, 30))
        tr2 = TimeRange(start=Time(10, 30), end=Time(11, 30))
        assert trid._one_is_in_other(tr2, tr1) is False

        tr1 = TimeRange(start=Time(11, 30), end=Time(12, 30))
        tr2 = TimeRange(start=Time(10, 30), end=Time(12, 00))
        assert trid._one_is_in_other(tr2, tr1) is False

        tr1 = TimeRange(start=Time(10, 30), end=Time(12, 30))
        tr2 = TimeRange(start=Time(12, 0), end=Time(13, 00))
        assert trid._one_is_in_other(tr2, tr1) is False

        tr1 = TimeRange(start=Time(10, 30), end=Time(14, 30))
        tr2 = TimeRange(start=Time(12, 0), end=Time(13, 00))
        assert trid._one_is_in_other(tr1, tr2) is False

        tr1 = TimeRange(start=Time(10, 30), end=Time(12, 30))
        tr2 = TimeRange(start=Time(12, 40), end=Time(13, 00))
        assert trid._one_is_in_other(tr2, tr1) is False

        tr1 = TimeRange(start=Time(12, 40), end=Time(15, 00))
        tr2 = TimeRange(start=Time(10, 30), end=Time(12, 30))
        assert trid._one_is_in_other(tr2, tr1) is False

    def test__other_ends_in_one__not(self, trid):
        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(10, 20), end=Time(14, 13))
        assert trid._other_ends_in_one(tr2, tr1) is False

        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(10, 20), end=Time(16, 13))
        assert trid._other_ends_in_one(tr2, tr1) is False

    def test__other_starts_in_one__not(self, trid):
        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(16, 12), end=Time(18, 20))
        assert trid._other_starts_in_one(tr2, tr1) is False

        tr1 = TimeRange(start=Time(14, 12), end=Time(17, 16))
        tr2 = TimeRange(start=Time(18, 19), end=Time(18, 20))
        assert trid._other_starts_in_one(tr1, tr2) is False

    def test__is_time_in_time_range__not(self, trid):
        t1 = Time(13, 1)
        tr2 = TimeRange(start=Time(10, 00), end=Time(13, 00))
        assert trid._is_time_in_time_range(tr2, t1) is False

        t1 = Time(10, 00)
        tr2 = TimeRange(start=Time(10, 00), end=Time(13, 00))
        assert trid._is_time_in_time_range(tr2, t1) is False

        t1 = Time(14, 20)
        tr2 = TimeRange(start=Time(10, 00), end=Time(13, 00))
        assert trid._is_time_in_time_range(tr2, t1) is False

        t1 = Time(8, 20)
        tr2 = TimeRange(start=Time(10, 00), end=Time(13, 00))
        assert trid._is_time_in_time_range(tr2, t1) is False

    def test__is_time_ranges_intersect__not(self, trid):
        tr1 = TimeRange(start=Time(9, 00), end=Time(10, 0))
        tr2 = TimeRange(start=Time(10, 00), end=Time(12, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is False

        tr1 = TimeRange(start=Time(12, 00), end=Time(13, 00))
        tr2 = TimeRange(start=Time(11, 00), end=Time(12, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is False

        tr1 = TimeRange(start=Time(10, 00), end=Time(11, 00))
        tr2 = TimeRange(start=Time(12, 00), end=Time(13, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is False

        tr1 = TimeRange(start=Time(15, 00), end=Time(16, 00))
        tr2 = TimeRange(start=Time(10, 00), end=Time(12, 00))
        assert trid._is_time_ranges_intersect(tr1, tr2) is False

    def test_is_intersection__not(self, trid):
        t = Time(9, 20)
        tr = TimeRange(start=Time(10, 00), end=Time(11, 00))
        assert trid.is_intersection(tr, t) is False

        tr1 = TimeRange(start=Time(11, 30), end=Time(12, 00))
        tr2 = TimeRange(start=Time(10, 00), end=Time(11, 00))
        assert trid.is_intersection(tr1, tr2) is False
