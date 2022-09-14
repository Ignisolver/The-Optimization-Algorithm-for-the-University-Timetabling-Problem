import pytest

from data_input.basic_structure_loader.basic_structure_loader_utils. \
    time_loader import TimeLoader
from time_ import TimeRange, Time
from utils.types_ import Day


@pytest.fixture
def tl() -> TimeLoader:
    return TimeLoader()


class TestTimeLoader:
    def test__create_ranges(self, tl):
        time = [[1, 2, 3], [10, 20], [15, 18]]
        time_ranges = tl._create_ranges(time)
        assert len(time_ranges) == 3
        assert TimeRange(Time(10, 20), Time(15, 18), day=Day(0)) in time_ranges
        assert TimeRange(Time(10, 20), Time(15, 18), day=Day(1)) in time_ranges
        assert TimeRange(Time(10, 20), Time(15, 18), day=Day(2)) in time_ranges

    def test__extract_ranges(self, tl):
        times = [[[1, 2, 3], [10, 20], [15, 18]],
                 [[2, 3], [1, 20], [16, 18]],
                 [[4, 5], [12, 20], [17, 18]],
                 [[1], [13, 20], [18, 18]]]
        time_ranges = tl._extract_ranges(times)
        assert len(time_ranges) == 8
        assert TimeRange(Time(10, 20), Time(15, 18), day=Day(2)) in time_ranges
        assert TimeRange(Time(13, 20), Time(18, 18), day=Day(0)) in time_ranges

    def test__assert_both_none(self, tl):
        assert tl._assert_both_none(None, 1) is False
        assert tl._assert_both_none(None, None) is True
        assert tl._assert_both_none(1, None) is False
        assert tl._assert_both_none(1, 1) is False

    def test__assert_both_not_none(self, tl):
        assert tl._assert_both_none(None, 1) is False
        assert tl._assert_both_none(None, None) is False
        assert tl._assert_both_none(1, None) is False
        assert tl._assert_both_none(1, 1) is True

    def test_get_ranges_or_none(self, tl):
        times = [[[4, 5], [12, 20], [17, 18]],
                 [[1], [13, 20], [18, 18]]]
        extracted_times = tl._get_ranges_or_none(times)
        assert len(extracted_times) == 3
        nan = tl._get_ranges_or_none(None)
        assert nan is None

    def test__extract_pref_times_3(self, tl):
        assert False

    def test__extract_pref_times_2(self, tl):
        raw_pref_times = [[[1, 2, 3], [10, 20], [15, 18]], 2]
        pref_times = tl._extract_pref_times_2(raw_pref_times)
        assert PreferredTime(TimeRange(Time(10, 20), Time(15, 18),
                                       day=Day(0)), 2) in pref_times
        assert PreferredTime(TimeRange(Time(10, 20), Time(15, 18),
                                       day=Day(1)), 2) in pref_times
        assert PreferredTime(TimeRange(Time(10, 20), Time(15, 18),
                                       day=Day(2)), 2) in pref_times

        
    def test__extract_pref_times_1(self, tl):
        raw_pref_times = [[[[1, 2, 3], [10, 20], [15, 18]], 2],
                          [[[1], [13, 20], [18, 18]], 10]]
        pref_times = tl._extract_pref_times_1(raw_pref_times)
        assert len(pref_times) == 4
        assert PreferredTime(TimeRange(Time(10, 20), Time(15, 18),
                                       day=Day(0)), 2) in pref_times
        assert PreferredTime(TimeRange(Time(10, 20), Time(15, 18),
                                       day=Day(1)), 2) in pref_times
        assert PreferredTime(TimeRange(Time(10, 20), Time(15, 18),
                                       day=Day(2)), 2) in pref_times
        assert PreferredTime(TimeRange(Time(13, 20), Time(18, 18),
                                       day=Day(0)), 10) in pref_times

    def test_load_pref_times(self, tl):
        raw_pref_times = [[[[1, 2, 3], [10, 20], [15, 18]], 2],
                          [[[1], [13, 20], [18, 18]], 10],
                          [[None, None, None], 6]]
        pref_times = tl.load_pref_times(raw_pref_times)
        assert len(pref_times) == 5
        assert PreferredTime(TimeRange(Time(10, 20), Time(15, 18),
                                       day=Day(0)), 2) in pref_times
        assert PreferredTime(TimeRange(Time(10, 20), Time(15, 18),
                                       day=Day(1)), 2) in pref_times
        assert PreferredTime(TimeRange(Time(10, 20), Time(15, 18),
                                       day=Day(2)), 2) in pref_times
        assert PreferredTime(TimeRange(Time(13, 20), Time(18, 18),
                                       day=Day(0)), 10) in pref_times
        assert PreferredTime(None, 6) in pref_times

    def test__assert_times_not_overlap(self, tl):
        assert False

    def test__assert_ranges_correct(self, tl):
        assert False

    def test_load_available_and_unavailable_times(self, tl):
        assert False
