import os
import types
from os import listdir, remove

from utils.constans import ROOT_PATH
import pickle

from utils.test_result import TestResult

folder_path = ROOT_PATH.joinpath("data_generation/config")

imported = False


def run(globals_, ret_code=False):
    dump_all(globals_)
    code = os.system("py -3.10 ../main.py")
    if ret_code:
        return load_res(), code
    return load_res()


def dump_all(globals_):
    for file in listdir(folder_path):
        remove(folder_path.joinpath(file))

    for name, var in globals_.items():
        if "__" not in name:
            if not isinstance(var, types.FunctionType):
                if not isinstance(var, types.ModuleType):
                    if name[0].lower() != name[0]:
                        dump(name, var)


def dump(name, variable):
    with open(folder_path.joinpath(name + ".bin"), 'wb') as file:
        pickle.dump(variable, file)


def load_res() -> TestResult:
    with open(ROOT_PATH.joinpath("results/result.bin"), 'rb') as file:
        res = pickle.load(file)
    return res
