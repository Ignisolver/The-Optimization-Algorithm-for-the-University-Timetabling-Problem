from pathlib import Path

from utils.types_ import (MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
                          FRIDAY)

DAYS = [MONDAY, TUESDAY, WEDNESDAY,
        THURSDAY, FRIDAY]

ROOT_PATH = Path(__file__).parent.parent.absolute()

BTW = "BRAKE_TIME_VAL"
WA = "WEEK_ARANGEMENT"
UNI = "UNIFORMITY"
DU = "DAYS_UNFOLDING"
