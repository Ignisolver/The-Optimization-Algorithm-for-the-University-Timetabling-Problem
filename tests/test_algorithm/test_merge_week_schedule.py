from algorithm.merge_week_schedule import (_filter_ranges_grater_or_equal_than,
                                           _get_common_ranges_from_two_list,
                                           _get_common_ranges,
                                           _merge_touching_available_ranges_in_day,
                                           _get_common_ranges_for_day,
                                           get_free_ranges_from_week_schedules,
                                           )
from algorithm.best_times_finder import _get_start_times, Start as S
from basic_structures import Classes, Room, Lecturer, Group
from basic_structures.with_schedule import WithSchedule
from data import MAX_HOUR
from time_ import TimeRange as TR, Time as T, TimeDelta as TD
from utils.types_ import (MONDAY as M,
                          TUESDAY as TU,
                          THURSDAY as TH,
                          ClassesType as CT,
                          FRIDAY as F,
                          WEDNESDAY as W)


def test__filter_times_grater_or_equal_than():
    times = [TR(T(1, 20), dur=TD(2, 0)),
             TR(T(1, 20), dur=TD(1, 30)),
             TR(T(1, 20), dur=TD(1, 0)),
             TR(T(1, 20), dur=TD(0, 50)),
             TR(T(1, 20), dur=TD(0, 10))]
    t = _filter_ranges_grater_or_equal_than(times, TD(1))
    assert len(t) == 3
    t = _filter_ranges_grater_or_equal_than(times, TD(1, 50))
    assert t[0] == times[0]


def test__get_common_ranges():
    tr = TR(start=T(10, 0), end=T(12, 0), day=M)
    tr1 = TR(start=T(8, 0), end=T(9, 0), day=M)
    tr2 = TR(start=T(9, 0), end=T(10, 0), day=M)
    tr3 = TR(start=T(9, 0), end=T(11, 00), day=M)
    tr4 = TR(start=T(9, 0), end=T(12, 0), day=M)
    tr5 = TR(start=T(9, 0), end=T(13, 0), day=M)
    tr6 = TR(start=T(10, 0), end=T(11, 0), day=M)
    tr7 = TR(start=T(10, 0), end=T(12, 0), day=M)
    tr8 = TR(start=T(10, 0), end=T(13, 0), day=M)
    tr9 = TR(start=T(11, 0), end=T(12, 0), day=M)
    tr10 = TR(start=T(11, 0), end=T(13, 0), day=M)
    tr11 = TR(start=T(12, 0), end=T(13, 0), day=M)
    tr12 = TR(start=T(13, 0), end=T(14, 0), day=M)

    assert _get_common_ranges(tr, tr1) == []
    assert _get_common_ranges(tr, tr2) == []
    assert _get_common_ranges(tr, tr3) == [
        TR(start=T(10, 0), end=T(11, 0), day=M)]
    assert _get_common_ranges(tr, tr4) == [
        TR(start=T(10, 0), end=T(12, 0), day=M)]
    assert _get_common_ranges(tr, tr5) == [
        TR(start=T(10, 0), end=T(12, 0), day=M)]
    assert _get_common_ranges(tr, tr6) == [
        TR(start=T(10, 0), end=T(11, 0), day=M)]
    assert _get_common_ranges(tr, tr7) == [
        TR(start=T(10, 0), end=T(12, 0), day=M)]
    assert _get_common_ranges(tr, tr8) == [
        TR(start=T(10, 0), end=T(12, 0), day=M)]
    assert _get_common_ranges(tr, tr9) == [
        TR(start=T(11, 0), end=T(12, 0), day=M)]
    assert _get_common_ranges(tr, tr10) == [
        TR(start=T(11, 0), end=T(12, 0), day=M)]
    assert _get_common_ranges(tr, tr11) == []
    assert _get_common_ranges(tr, tr12) == []


def test__get_common_ranges_from_two_list():
    trl1 = [TR(start=T(8, 0), end=T(10, 0), day=M),
            TR(start=T(13, 0), end=T(14, 0), day=M),
            TR(start=T(16, 0), end=T(17, 0), day=M),
            TR(start=T(19, 0), end=T(20, 0), day=M),
            ]
    trl2 = [TR(start=T(8, 0), end=T(11, 0), day=M),
            TR(start=T(12, 0), end=T(12, 30), day=M),
            TR(start=T(12, 50), end=T(13, 50), day=M),
            TR(start=T(18, 30), end=T(19, 30), day=M),
            ]
    trl3 = []
    expected_trs = [TR(start=T(8, 0), end=T(10, 0), day=M),
                    TR(start=T(13, 0), end=T(13, 50), day=M),
                    TR(start=T(19, 0), end=T(19, 30), day=M)
                    ]
    trs = _get_common_ranges_from_two_list(trl1, trl2)
    assert trs == expected_trs
    assert _get_common_ranges_from_two_list(trs, trl3) == []


def test__merge_touching_available_ranges_in_day():
    trs1 = [TR(start=T(8, 0), end=T(11, 0), day=M),
            TR(start=T(12, 0), end=T(13, 0), day=M),
            TR(start=T(13, 00), end=T(14, 0), day=M),
            TR(start=T(18, 30), end=T(19, 30), day=M),
            ]
    trs2 = [TR(start=T(8, 0), end=T(11, 0), day=M),
            TR(start=T(12, 0), end=T(13, 0), day=M),
            TR(start=T(13, 00), end=T(14, 0), day=M),
            ]
    trs3 = []

    m1 = _merge_touching_available_ranges_in_day(trs1)
    m2 = _merge_touching_available_ranges_in_day(trs2)
    m3 = _merge_touching_available_ranges_in_day(trs3)

    expected_m1 = [TR(start=T(8, 0), end=T(11, 0), day=M),
                   TR(start=T(12, 0), end=T(14, 0), day=M),
                   TR(start=T(18, 30), end=T(19, 30), day=M),
                   ]
    expected_m2 = [TR(start=T(8, 0), end=T(11, 0), day=M),
                   TR(start=T(12, 0), end=T(14, 0), day=M),
                   ]
    expected_m3 = []

    assert m1 == expected_m1
    assert m2 == expected_m2
    assert m3 == expected_m3


def test__get_common_ranges_for_day():
    trs1 = [TR(start=T(8, 0), end=T(11, 0), day=M),
            TR(start=T(13, 0), end=T(15, 0), day=M),
            TR(start=T(18, 0), end=T(19, 0), day=M),
            ]
    trs2 = [TR(start=T(9, 0), end=T(12, 0), day=M),
            TR(start=T(12, 30), end=T(14, 0), day=M),
            TR(start=T(18, 30), end=T(20, 0), day=M),
            ]
    trs3 = [TR(start=T(8, 30), end=T(9, 30), day=M),
            TR(start=T(13, 20), end=T(14, 0), day=M),
            TR(start=T(17, 0), end=T(18, 30), day=M),
            ]
    trs = _get_common_ranges_for_day([trs1, trs2, trs3], TD(0, 10))
    expected_trs = [TR(start=T(9, 0), end=T(9, 30), day=M),
                    TR(start=T(13, 20), end=T(14, 00), day=M)]
    assert trs == expected_trs

    trs = _get_common_ranges_for_day([trs1, trs2, trs3], TD(0, 30))
    expected_trs = [TR(start=T(9, 0), end=T(9, 30), day=M),
                    TR(start=T(13, 20), end=T(14, 00), day=M)]
    assert trs == expected_trs

    trs = _get_common_ranges_for_day([trs1, trs2, trs3], TD(0, 40))
    expected_trs = [TR(start=T(13, 20), end=T(14, 00), day=M),]
    assert trs == expected_trs

    trs = _get_common_ranges_for_day([trs1, trs2, trs3], TD(1, 40))
    expected_trs = []
    assert trs == expected_trs


class WWMock(WithSchedule):
    pass


def test__get_ranges_from_week_schedules():
    a = WWMock()
    cls = [Classes(1, "C", TD(1, 0), CT.LECTURE, [Room(1, 1, 1)],
                   Lecturer(1, "L"),
                   [Group(1, "G", 10)], Room(1, 1, 1)) for _ in range(10)]
    start_hours = [T(8, 0), T(10, 0), T(11, 0), T(15, 0),
                   T(8, 0), T(10, 0), T(11, 0),
                   T(8, 0), T(10, 0), T(11, 0),
                   ]
    days = [M, M, M, M, W, W, W, F, F, F]
    for cl, hour, day in zip(cls, start_hours, days):
        cl.assign(hour, Room(1, 1, 1), day)
        a.week_schedule.assign(cl)

    b = WWMock()
    cls = [Classes(1, "C", TD(1, 0), CT.LECTURE, [Room(1, 1, 1)],
                   Lecturer(1, "L"),
                   [Group(1, "G", 10)], Room(1, 1, 1)) for _ in range(10)]
    start_hours = [T(9, 0), T(10, 0), T(13, 0), T(19, 0),
                   T(11, 0), T(13, 0), T(15, 0),
                   T(8, 0), T(11, 0), T(14, 0),
                   ]
    days = [M, M, M, M, W, W, W, F, F, F]
    for cl, hour, day in zip(cls, start_hours, days):
        cl.assign(hour, Room(1, 1, 1), day)
        b.week_schedule.assign(cl)

    c = WWMock()
    cls = [Classes(1, "C", TD(1, 0), CT.LECTURE, [Room(1, 1, 1)],
                   Lecturer(1, "L"),
                   [Group(1, "G", 10)], Room(1, 1, 1)) for _ in range(10)]
    start_hours = [T(8, 0), T(10, 0), T(11, 0), T(15, 0),
                   T(10, 0), T(11, 0), T(15, 0), T(17, 0), T(19, 0),
                   T(16, 0),
                   ]
    days = [TU] * 4 + [TH] * 5 + [F]
    for cl, hour, day in zip(cls, start_hours, days):
        cl.assign(hour, Room(1, 1, 1), day)
        c.week_schedule.assign(cl)

    rgs = get_free_ranges_from_week_schedules([a, b, c], TD())
    exp_rgs = [TR(start=T(12, 0), end=T(13, 0), day=M),
               TR(start=T(14, 0), end=T(15, 0), day=M),
               TR(start=T(16, 0), end=T(19, 0), day=M),
               TR(start=T(20, 0), end=MAX_HOUR, day=M),
               TR(start=T(9, 0), end=T(10, 0), day=TU),
               TR(start=T(12, 0), end=T(15, 0), day=TU),
               TR(start=T(16, 0), end=MAX_HOUR, day=TU),
               TR(start=T(9, 0), end=T(10, 0), day=W),
               TR(start=T(12, 0), end=T(13, 0), day=W),
               TR(start=T(14, 0), end=T(15, 0), day=W),
               TR(start=T(16, 0), end=MAX_HOUR, day=W),
               TR(start=T(8, 0), end=T(10, 0), day=TH),
               TR(start=T(12, 0), end=T(15, 0), day=TH),
               TR(start=T(16, 0), end=T(17, 0), day=TH),
               TR(start=T(18, 0), end=T(19, 0), day=TH),
               TR(start=T(20, 0), end=MAX_HOUR, day=TH),
               TR(start=T(9, 0), end=T(10, 0), day=F),
               TR(start=T(12, 0), end=T(14, 0), day=F),
               TR(start=T(15, 0), end=T(16, 0), day=F),
               TR(start=T(17, 0), end=MAX_HOUR, day=F),
               ]

    rgs2 = get_free_ranges_from_week_schedules((a, b, c), TD(2, 0))
    exp_rgs2 = [
        TR(start=T(16, 0), end=T(19, 0), day=M),
        TR(start=T(12, 0), end=T(15, 0), day=TU),
        TR(start=T(16, 0), end=MAX_HOUR, day=TU),
        TR(start=T(16, 0), end=MAX_HOUR, day=W),
        TR(start=T(8, 0), end=T(10, 0), day=TH),
        TR(start=T(12, 0), end=T(15, 0), day=TH),
        TR(start=T(12, 0), end=T(14, 0), day=F),
        TR(start=T(17, 0), end=MAX_HOUR, day=F),
        ]
    assert rgs2 == exp_rgs2


def test_get_start_times():
    ranges = [
        TR(start=T(8, 0), end=T(10, 0), day=M),
        TR(start=T(13, 0), end=T(14, 0), day=M),
        TR(start=T(15, 0), end=T(18, 0), day=M),
    ]
    starts = _get_start_times(ranges, dur=TD(1))
    expected_starts = [
        S(T(8,00), M),S(T(8,10), M),S(T(8,20), M),S(T(8,30), M),S(T(8,40), M),S(T(8,50), M),S(T(9,0), M),S(T(13,0), M),
        S(T(15, 0), M),S(T(15,10), M),S(T(15,20), M),S(T(15,30), M),S(T(15,40), M),S(T(15,50), M),S(T(16, 00), M),
        S(T(16, 10), M),S(T(16, 20), M),S(T(16, 30), M),S(T(16, 40), M),S(T(16, 50), M), S(T(17, 0),M)]
    assert starts == expected_starts
