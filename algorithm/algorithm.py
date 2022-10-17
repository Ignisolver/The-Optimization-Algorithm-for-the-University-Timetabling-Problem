from typing import List

from time_ import TimeDelta


def filter_times_grater_then(times: List[TimeDelta], dur: TimeDelta):
    return tuple(filter(lambda td: td >= dur, times))
    # testme
