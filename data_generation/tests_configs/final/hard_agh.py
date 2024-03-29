from time_ import Time, TimeDelta
from utils.constans import BTW, WA, UNI, DU

NAME = "AGH"
AMOUNT_OF_FIELDS = 232
AMOUNT_OF_GROUPS_IN_FIELD = 12*[3]+3*[5]+[2]
SUBJECTS_PER_FIELD = [7]
AMOUNT_OF_STUDENTS_PER_GROUP = [30, 20, 25, 30]
AMOUNT_OF_LECTURERS = 1400
AMOUNT_OF_BUILDINGS = 25
DISTANCES_BETWEEN_BUILDINGS = [5, 10, 5,10,15]
AMOUNT_OF_LAB_ROOMS = 19*[17]+[21]
AMOUNT_OF_LECT_ROOMS = 19*[10]+[6]
LAB_ROOMS_CAPACITIES = [max(AMOUNT_OF_STUDENTS_PER_GROUP)]
LECTURE_ROOM_CAPACITIES = [
    max(AMOUNT_OF_GROUPS_IN_FIELD) * max(AMOUNT_OF_STUDENTS_PER_GROUP)]
AMOUNT_OF_RANDOM_UNAVAILABILITY_FOR_ROOMS = 20 * [0] + [1]
AMOUNT_OF_RANDOM_UNAVAILABILITY_FOR_LECTURERS = [1, 0]
UNAVAILABILITY_DURATION_ROOMS = [360]
UNAVAILABILITY_DURATION_LECTURERS = [180]
DURATIONS_OF_CLASSES = 30 * [90] + 5*[120] + [180]
AVAILABLE_ROOMS_AMOUNT = 15*[15]+5*[6]+[5]
# ----------------------------------------------------------------------------
MIN_HOUR = Time(8, 0)
MAX_HOUR = Time(20, 0)
TIME_GRANULATION = TimeDelta(0, 5)  # (1, 2, 5, 10, 15, 20, 30, 60)
WEEK_LENGTH_MIN = 5 * int(MAX_HOUR - MIN_HOUR)
MAX_TIME_PER_DAY = int(TimeDelta(8, 0))
DAY_TIME_WEIGHTS = [0, 1, 2,3,5,6,7,8,9,10,11, 12]
GOAL_FUNCTION_WEIGHTS = {BTW: 5, WA: 1, UNI: 5, DU: 0.1}
TIME_BETWEEN_ROOMS = TimeDelta(0, 5)
GEN = True
