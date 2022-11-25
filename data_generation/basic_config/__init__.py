from utils.constans import ROOT_PATH
from os import listdir

import pickle
folder_path = ROOT_PATH.joinpath("data_generation/configs")

for file_name in listdir(folder_path):
    name = file_name[:-4]
    file_path = folder_path.joinpath(file_name)
    with open(file_path, 'rb') as file:
        globals()[name] = pickle.load(file)
