from time_ import Time, TimeDelta
from utils.constans import ROOT_PATH, BTW, WA, UNI, DU
from os import listdir

import pickle
folder_path = ROOT_PATH.joinpath("data_generation/config")

for file_name in listdir(folder_path):
    name = file_name[:-4]
    file_path = folder_path.joinpath(file_name)
    with open(file_path, 'rb') as file:
        globals()[name] = pickle.load(file)

if __name__ == '__main__':
    NAME = "INCORRECT IMPORT"
    AMOUNT_OF_FIELDS = 1
    AMOUNT_OF_GROUPS_IN_FIELD = [2]
    SUBJECTS_PER_FIELD = [8]
    AMOUNT_OF_STUDENTS_PER_GROUP = [30]
    AMOUNT_OF_LECTURERS = 1
    AMOUNT_OF_BUILDINGS = 1
    DISTANCES_BETWEEN_BUILDINGS = [0]
    AMOUNT_OF_LAB_ROOMS = [1]
    AMOUNT_OF_LECT_ROOMS = [1]
    LAB_ROOMS_CAPACITIES = [max(AMOUNT_OF_STUDENTS_PER_GROUP)]
    LECTURE_ROOM_CAPACITIES = [
        max(AMOUNT_OF_GROUPS_IN_FIELD) * max(AMOUNT_OF_STUDENTS_PER_GROUP)]
    AMOUNT_OF_RANDOM_UNAVAILABILITY_FOR_ROOMS = [0]
    AMOUNT_OF_RANDOM_UNAVAILABILITY_FOR_LECTURERS = [0]
    UNAVAILABILITY_DURATION_ROOMS = [0]
    UNAVAILABILITY_DURATION_LECTURERS = [0]
    DURATIONS_OF_CLASSES = [90]
    AVAILABLE_ROOMS_AMOUNT = [1]
    # ----------------------------------------------------------------------------
    MIN_HOUR = Time(8, 0)
    MAX_HOUR = Time(20, 0)
    TIME_GRANULATION = TimeDelta(0, 10)  # (1, 2, 5, 10, 15, 20, 30, 60)
    WEEK_LENGTH_MIN = 5 * int(MAX_HOUR - MIN_HOUR)
    MAX_TIME_PER_DAY = int(TimeDelta(8, 0))
    DAY_TIME_WEIGHTS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    GOAL_FUNCTION_WEIGHTS = {BTW: 5, WA: 1, UNI: 5, DU: 0.1}
    TIME_BETWEEN_ROOMS = TimeDelta(0, 5)
    GEN = True