import types
from os import listdir, remove

from utils.constans import ROOT_PATH
import pickle

folder_path = ROOT_PATH.joinpath("data_generation/configs")
from importlib import reload

imported = False


def load_main():
    if not imported:
        import main
    reload(main)
    main_f = main.main
    return main_f


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


def load_res():
    with open(ROOT_PATH.joinpath("results/result.bin"), 'rb') as file:
        res = pickle.load(file)
    return res
