from time_ import Time, TimeDelta
from utils.constans import BTW, WA, UNI, DU

NAME = "DIFFICULT"
AMOUNT_OF_FIELDS = 100
AMOUNT_OF_GROUPS_IN_FIELD = [5]
SUBJECTS_PER_FIELD = [8]
AMOUNT_OF_STUDENTS_PER_GROUP = [30, 20, 25, 30]
AMOUNT_OF_LECTURERS = 204
AMOUNT_OF_BUILDINGS = 8
DISTANCES_BETWEEN_BUILDINGS = [5, 10, 5, 5, 10, 20, 15, 5]
AMOUNT_OF_LAB_ROOMS = [29, 10, 25, 19, 19]
AMOUNT_OF_LECT_ROOMS = [3, 3, 5, 7, 4]
LAB_ROOMS_CAPACITIES = [max(AMOUNT_OF_STUDENTS_PER_GROUP)]
LECTURE_ROOM_CAPACITIES = [
    max(AMOUNT_OF_GROUPS_IN_FIELD) * max(AMOUNT_OF_STUDENTS_PER_GROUP)]
AMOUNT_OF_RANDOM_UNAVAILABILITY_FOR_ROOMS = 20 * [0] + [1]
AMOUNT_OF_RANDOM_UNAVAILABILITY_FOR_LECTURERS = [1, 0]
UNAVAILABILITY_DURATION_ROOMS = [360]
UNAVAILABILITY_DURATION_LECTURERS = [360]
DURATIONS_OF_CLASSES = 30 * [90] + 5*[120]
AVAILABLE_ROOMS_AMOUNT = [15]
# ----------------------------------------------------------------------------
MIN_HOUR = Time(8, 0)
MAX_HOUR = Time(20, 0)
TIME_GRANULATION = TimeDelta(0, 10)  # (1, 2, 5, 10, 15, 20, 30, 60)
WEEK_LENGTH_MIN = 5 * int(MAX_HOUR - MIN_HOUR)
MAX_TIME_PER_DAY = int(TimeDelta(8, 0))
DAY_TIME_WEIGHTS = [0, 1, 2, 3,4,5,6,7,8,9,10,11, 12]
GOAL_FUNCTION_WEIGHTS = {BTW: 10, WA: 40, UNI: 1, DU: 10}
TIME_BETWEEN_ROOMS = TimeDelta(0, 5)
GEN = True
