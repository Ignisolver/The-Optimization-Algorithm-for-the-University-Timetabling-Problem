from time_ import Time, TimeDelta
from utils.constans import BTW, WA, UNI, DU

# TEST
MIN_HOUR = Time(8, 0)
MAX_HOUR = Time(21, 0)

WEEK_LENGTH_MIN = 5 * int(MAX_HOUR - MIN_HOUR)

MAX_TIME_PER_DAY = TimeDelta(8, 0)

DAY_TIME_WEIGHTS = [0, 1, 1, 2, 2, 3, 4, 5, 6, 7, 9, 12, 20]

GOAL_FUNCTION_WEIGHTS = {BTW: 1, WA: 1, UNI: 1, DU: 1}

TIME_BETWEEN_ROOMS = 5

# ----------------------------------------------------------------
