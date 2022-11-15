from time_ import TimeDelta, Time
from utils.constans import BTW, WA, UNI, DU

NAME = "TEST"
AMOUNT_OF_FIELDS = 10
AMOUNT_OF_GROUPS_IN_FIELD = [6, 8, 4, 2]
SUBJECTS_PER_FIELD = [8, 8, 7, 6]
AMOUNT_OF_STUDENTS_PER_GROUP = 8 * [30] + 2 * [15]
AMOUNT_OF_LECTURERS = 40
AMOUNT_OF_BUILDINGS = 4
DISTANCES_BETWEEN_BUILDINGS = 2 * [10] + 2 * [20]
AMOUNT_OF_LAB_ROOMS = [5, 4, 8, 6]
AMOUNT_OF_LECT_ROOMS = [2, 1, 3, 1]
LAB_ROOMS_CAPACITIES = [max(AMOUNT_OF_STUDENTS_PER_GROUP)]
LECTURE_ROOM_CAPACITIES = [
    max(AMOUNT_OF_GROUPS_IN_FIELD) * max(AMOUNT_OF_STUDENTS_PER_GROUP)]
AMOUNT_OF_RANDOM_UNAVAILABILITY_FOR_ROOMS = 10 * [0] + 2 * [1] + [2]
AMOUNT_OF_RANDOM_UNAVAILABILITY_FOR_LECTURERS = 5 * [0] + 5 * [1] + 4 * [2]
UNAVAILABILITY_DURATION_ROOMS = 4 * [60 * 4] + 2 * [60 * 8]
UNAVAILABILITY_DURATION_LECTURERS = 4 * [60 * 4] + 2 * [60 * 2]
DURATIONS_OF_CLASSES = 3 * [90] + [60, 120]
AVAILABLE_ROOMS_AMOUNT = 10 * [1] + 5 * [2] + 20 * [10]
# -------------------------------------------------####
MIN_HOUR = Time(8, 0)
MAX_HOUR = Time(21, 0)
TIME_GRANULATION = TimeDelta(0, 10)  # (1, 2, 5, 10, 15, 20, 30, 60)
WEEK_LENGTH_MIN = 5 * int(MAX_HOUR - MIN_HOUR)
MAX_TIME_PER_DAY = int(TimeDelta(8, 0))
DAY_TIME_WEIGHTS = [0, 1, 1, 2, 2, 3, 4, 5, 6, 7, 9, 12, 20]
GOAL_FUNCTION_WEIGHTS = {BTW: 1, WA: 1, UNI: 1, DU: 1}
TIME_BETWEEN_ROOMS = TimeDelta(0, 10)