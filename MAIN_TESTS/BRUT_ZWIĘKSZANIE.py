from itertools import cycle
from math import log

from MAIN_TESTS.change_config import run
from data_generation.tests_configs.final.hard_agh import *

# READY


def sum_rooms(rooms):
    val = 0
    rooms = cycle(rooms)
    for i in range(AMOUNT_OF_BUILDINGS):
        val += next(rooms)
    return val


room_usages = []
lect_usages = []
successes = []
failures = []
gfv_s = []
gfv_components = []

mul = 5
LAB_STEP = AMOUNT_OF_LAB_ROOMS[0]/10
LECT_STEP = LAB_STEP * 80/400
ratio = 0.9

labs_r_min = AMOUNT_OF_LAB_ROOMS[0]
lect_r_min = AMOUNT_OF_LECT_ROOMS[0]
lect_min = AMOUNT_OF_LECTURERS
AMOUNT_OF_LECTURERS = mul * lect_min
first_amount_of_labs_rooms = AMOUNT_OF_LAB_ROOMS[0]
first_amount_of_lect_rooms = AMOUNT_OF_LECT_ROOMS[0]

LECT_VAL = lect_r_min
LAB_VAl = labs_r_min

end = False

iter_am = int(log(1/mul)/log(ratio))
print(iter_am)

for i in range(iter_am):
    while True:
        print("LECTS ", AMOUNT_OF_LECT_ROOMS[0])
        print("LABS  ", AMOUNT_OF_LAB_ROOMS[0])
        print("L     ", AMOUNT_OF_LECTURERS)

        res, code = run(globals(), ret_code=True)

        print("S", res.successes)
        print("F", res.failures)
        print(20 * "-")
        LAB_VAl += LAB_STEP
        LECT_VAL += LECT_STEP

        AMOUNT_OF_LAB_ROOMS[0] = int(LAB_VAl)
        AMOUNT_OF_LECT_ROOMS[0] = int(LECT_VAL)

        if res.failures == 0:
            LAB_VAl -= LAB_STEP
            LECT_VAL -= LECT_STEP
            break
        if res.rooms_usage_before < 30:
            end = True
            break
        if code != 0:
            end = True
            break

    if end:
        break
    else:
        room_usages.append(res.rooms_usage_before)
        lect_usages.append(res.lecturers_usage_before)
        successes.append(res.successes)
        failures.append(res.failures)
        gfv_s.append(res.mean_gfv)
        gfv_components.append((res.btw, res.uni, res.wa, res.du))

    AMOUNT_OF_LECTURERS = int(ratio*AMOUNT_OF_LECTURERS)
    print(AMOUNT_OF_LECT_ROOMS, AMOUNT_OF_LAB_ROOMS, first_amount_of_lect_rooms, first_amount_of_labs_rooms)
    print("RES", room_usages, lect_usages, successes, failures, sep="\n")
