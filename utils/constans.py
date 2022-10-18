from pathlib import Path

from utils.types_ import (MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
                          FRIDAY, SATURDAY, SUNDAY)


DAYS = [MONDAY, TUESDAY, WEDNESDAY,
        THURSDAY, FRIDAY, SATURDAY, SUNDAY]

ROOT_PATH = Path(__file__).parent.parent.absolute()

BTW = "BRAKE_TIME_VAL"
WA = "WEEK_ARANGEMENT"
UNI = "UNIFORMITY"
DU = "DAYS_UNFOLDING"