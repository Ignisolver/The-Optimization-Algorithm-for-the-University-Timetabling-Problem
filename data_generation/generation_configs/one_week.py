from time_ import Time, TimeDelta
from utils.constans import BTW, WA, UNI, DU

NAME = "ONE WEEK"
AMOUNT_OF_FIELDS = 1
AMOUNT_OF_GROUPS_IN_FIELD = [1]
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
UNAVAILABILITY_DURATION_ROOMS = [120]
UNAVAILABILITY_DURATION_LECTURERS = [120]
DURATIONS_OF_CLASSES = 3 * [90] + [60, 120]
AVAILABLE_ROOMS_AMOUNT = [2]
# -------------------------------------------------####
MIN_HOUR = Time(8, 0)
MAX_HOUR = Time(21, 0)
TIME_GRANULATION = TimeDelta(0, 10)  # (1, 2, 5, 10, 15, 20, 30, 60)
WEEK_LENGTH_MIN = 5 * int(MAX_HOUR - MIN_HOUR)
MAX_TIME_PER_DAY = int(TimeDelta(8, 0))
DAY_TIME_WEIGHTS = [0, 1, 2, 4, 6, 9, 18]
GOAL_FUNCTION_WEIGHTS = {BTW: 1, WA: 100, UNI: 1, DU: 1}
TIME_BETWEEN_ROOMS = TimeDelta(0, 5)
MOVE_TIME_ENABLE = True
