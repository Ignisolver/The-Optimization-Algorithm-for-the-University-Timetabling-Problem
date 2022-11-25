from time import time

import pytest

from algorithm.goal_function import iterator_over_day, Metric
from basic_structures import Classes, Lecturer as Lect, Room
from basic_structures.classes import UnavailableClasses
from data_generation.basic_config import DAY_TIME_WEIGHTS, \
    GOAL_FUNCTION_WEIGHTS
from schedule.week_scheadule import WeekSchedule
from time_ import Time as Tim, TimeDelta as TD
from utils.constans import DU, BTW, WA, UNI
from utils.types_ import MONDAY, ClassesType as CT, THURSDAY, FRIDAY



@pytest.fixture(scope="class")
def metric():
    start, dur, day = Tim(12, 30), TD(1, 0), MONDAY
    ws = WeekSchedule([UnavailableClasses(1, start, dur, day)])
    classes = [Classes(1, "a", TD(1, 0), CT.LECTURE, [], Lect(1, "l"), [], room=Room(1,1,1)),
               Classes(2, "a", TD(1, 0), CT.LECTURE, [], Lect(1, "l"), [], room=Room(1,1,1)),
               Classes(3, "a", TD(1, 0), CT.LECTURE, [], Lect(1, "l"), [], room=Room(1,1,1)),
               Classes(4, "a", TD(1, 0), CT.LECTURE, [], Lect(1, "l"), [], room=Room(1,1,1)),
               Classes(5, "a", TD(1, 0), CT.LECTURE, [], Lect(1, "l"), [], room=Room(1,1,1))]
    for i in range(len(classes))[:2]:
        classes[i].day = THURSDAY

    for i in range(len(classes))[2:]:
        classes[i].day = FRIDAY
    iod = iterator_over_day()
    for i in range(len(classes)):
        classes[i].start_time = next(iod)[0]
        next(iod)
        ws.assign(classes[i])
    ws.assigned_classes_time = 5 * 60
    ws.assigned_classes_amount = 5
    m = Metric(ws)
    return m


class TestMetric:
    def test__calc_worst_brake_time(self, metric):
        metric._calc_worst_brake_time()
        assert metric._worst_brake_time == 60 * 60

    def test__calc_medium_unfolding(self, metric):
        metric._calc_medium_unfolding()
        assert metric._medium_unfolding == 300

    def test__calc_worst_uniformity(self, metric):
        metric._calc_worst_uniformity()
        assert metric._worst_uniformity == 1500

    def test__calc_worst_days_unfolding(self, metric):
        metric._calc_worst_days_unfolding()
        assert metric._worst_days_unfolding == 100

    def test__calc_days_unfolding(self, metric):
        d_a = metric._calc_days_unfolding()
        assert d_a == 13 / 100

    def test__calc_brake_time_value(self, metric):
        bt = metric._calc_brake_time_value()
        assert bt == (3 * 60 - 0) / (60 * 60)

    def test__calc_week_arrangement(self, metric):
        wa = metric._calc_week_arrangement()
        assert wa == 2 / 7

    def test__calc_uniformity(self, metric):
        uni = metric._calc_uniformity()
        assert uni == (300 - 120 + 300 - 180) / 1500

    def test__calc_all_basics(self, metric):
        metric._calc_all_basics()

    def test_calc_goal_fcn(self, metric):
        gfv = metric.calc_goal_fcn()
        sum_ = 13 / 100 * GOAL_FUNCTION_WEIGHTS[DU]
        sum_ += (3 * 60 - 0) / (60 * 60) * GOAL_FUNCTION_WEIGHTS[BTW]
        sum_ += 2 / 7 * GOAL_FUNCTION_WEIGHTS[WA]
        sum_ += (300 - 120 + 300 - 180) / 1500 * GOAL_FUNCTION_WEIGHTS[UNI]
        assert round(gfv, 5) == round(sum_, 5)

    def test_time(self, metric):
        st = time()
        for i in range(1000):
            gfv = metric.calc_goal_fcn()
        et = time()
        print('\nGoal function speed: ', (et - st), "/ 1000")
