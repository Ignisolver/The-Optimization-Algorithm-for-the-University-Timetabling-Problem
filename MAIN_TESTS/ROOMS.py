import os
from MAIN_TESTS.change_config import dump_all, load_res, run

from data_generation.tests_configs.final.time_gran import *

feils = []
succ = []
times = []
AMOUNT_OF_LECT_ROOMS[0] = int(AMOUNT_OF_LECT_ROOMS[0] * 1.2)
AMOUNT_OF_LAB_ROOMS[0] = int(AMOUNT_OF_LAB_ROOMS[0] * 1.2)
AMOUNT_OF_LECTURERS = int(AMOUNT_OF_LECTURERS * 1.4)

for tg in (5, 10, 15, 20, 30, 45, 60, 90, 120):
    TIME_GRANULATION = TimeDelta(0, tg)
    res = run(globals())
    feils.append(res.failures)
    succ.append(res.successes)
    times.append(res.time)

    print(feils)
    print(succ)
    print(times)
