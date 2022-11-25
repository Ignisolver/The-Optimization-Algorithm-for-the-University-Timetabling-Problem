import pickle

from utils.constans import ROOT_PATH


def dump(variable):
    with open(ROOT_PATH.joinpath("results/result.bin"), 'wb') as file:
        pickle.dump(variable, file)