import os
from MAIN_TESTS.change_config import dump_all, load_res

from data_generation.tests_configs.goal_func_tests.all import *


usages = []
for buildings_am in [1,2,3,4,5]:
    AMOUNT_OF_BUILDINGS = buildings_am
    GEN = False
    dump_all(globals())
    os.system("py -3.10 main.py")
    res = load_res()
    usages.append(res)

