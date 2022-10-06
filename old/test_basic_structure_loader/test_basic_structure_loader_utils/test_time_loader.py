import pytest

from old.data_input.basic_structure_loader.basic_structure_loader_utils.time_loader import TimeLoader, PrefTime
from time_ import TimeRange, Time
from utils.types_ import Day


@pytest.fixture
def tl() -> TimeLoader:
    return TimeLoader()


tr1d = [1, [10, 20], [11, 40]]
tr2d = [5, [14, 34], [17, 00]]
tr1 = TimeRange(Time(10, 20), Time(11, 40), day=Day(0))
tr2 = TimeRange(Time(14, 34), Time(17, 00), day=Day(4))


class TestTimeLoader:
    def test__assert_aval_ranges_correct__ok(self, tl):
        tl._assert_aval_ranges_correct([tr1, tr2], None)
        tl._assert_aval_ranges_correct(None, [tr1, tr2])

    def test__assert_aval_ranges_correct__both_none(self, tl):
        with pytest.raises(AssertionError):
            tl._assert_aval_ranges_correct(None, None)

    def test__assert_aval_ranges_correct__overlap(self, tl):
        tr3 = TimeRange(Time(15, 34), Time(18, 00), day=Day(4))
        with pytest.raises(AssertionError):
            tl._assert_aval_ranges_correct(None, [tr1, tr2, tr3])

    def test__assert_ranges_not_overlap(self, tl):
        tr3 = TimeRange(Time(15, 34), Time(18, 00), day=Day(4))
        with pytest.raises(AssertionError):
            tl._assert_ranges_not_overlap([tr1, tr2, tr3])
        with pytest.raises(AssertionError):
            tl._assert_ranges_not_overlap([PrefTime(tr1, 2),
                                           PrefTime(tr2, 3),
                                           PrefTime(tr3, 20)])

        tl._assert_ranges_not_overlap([tr1, tr2])
        tl._assert_ranges_not_overlap([PrefTime(tr1, 2),
                                       PrefTime(tr2, 3)])

    def test__assert_one_none(self, tl):
        tl._assert_one_none(None, 1)
        tl._assert_one_none(1, None)
        with pytest.raises(AssertionError):
            tl._assert_one_none(None, None)
        with pytest.raises(AssertionError):
            tl._assert_one_none(1, 1)

    def test__get_range__ok(self, tl):
        r1 = tl._get_range(tr1d)
        assert r1 == tr1
        r2 = tl._get_range(tr2d)
        assert r2 == tr2
        r3 = tl._get_range(None)
        assert r3 is None

    def test__get_range__incorrect_input(self, tl):
        with pytest.raises(ValueError):
            tl._get_range(44)

    def test__get_ranges(self, tl):
        r_s_d = [tr1d, tr2d]
        r_s = tl._get_ranges(r_s_d)
        assert tr1 in r_s
        assert tr2 in r_s
        r_s_d_2 = tl._get_ranges(None)
        assert r_s_d_2 is None

    def test__get_pref_time(self, tl):
        ptd1 = [tr1d, 10]
        pt1 = tl._get_pref_time(ptd1)
        assert pt1 == PrefTime(tr1, 10)

        ptd2 = [tr2d, 10]
        pt2 = tl._get_pref_time(ptd2)
        assert pt2 == PrefTime(tr2, 10)

        ptd3 = [None, 10]
        pt3 = tl._get_pref_time(ptd3)
        assert pt3 == PrefTime(None, 10)

        ptd4 = [None, ]
        pt4 = tl._get_pref_time(ptd4)
        assert pt4 == PrefTime(None, 0)

    def test_load_pref_times(self, tl):
        d_t_l = [[tr1d, 2],
                 [tr2d, 4],
                 [None, 10]]
        p_d_t = tl.load_pref_times(d_t_l)
        assert PrefTime(*d_t_l[0]) in p_d_t
        assert PrefTime(*d_t_l[1]) in p_d_t
        assert PrefTime(None, 10) in p_d_t

        assert tl.load_pref_times(None) == PrefTime(None, 0)

    def test_load_times(self, tl):
        d_t_l = [tr1d, tr2d]
        av, unav = tl.load_times(d_t_l, None)
        assert TimeRange(*d_t_l[0]) in av
        assert TimeRange(*d_t_l[1]) in av
        assert unav is None

        av, unav = tl.load_times(None, unav)
        assert TimeRange(*d_t_l[0]) in unav
        assert TimeRange(*d_t_l[1]) in unav
        assert av is None


class TestPrefTime:
    def test_to_generate(self):
        pt = PrefTime(tr1, 2)
        assert pt.to_generate() == [tr1d, 2]
        pt = PrefTime(None, 3)
        assert pt.to_generate() == [None, 3]

    def test__get_tr_list(self):
        pt1 = PrefTime(tr1, 2)
        assert pt1._get_tr_list() == tr1d
        pt2 = PrefTime(None, 3)
        assert pt2._get_tr_list() is None

