import os
from MAIN_TESTS.change_config import dump_all, load_res, run

from data_generation.tests_configs.final.hard_agh import *

# GOAL_FUNCTION_WEIGHTS = {BTW: 4,  WA: 7, UNI: 5, DU: 5}

res = run(globals())

print(res.failures, print(res.failures+res.successes))