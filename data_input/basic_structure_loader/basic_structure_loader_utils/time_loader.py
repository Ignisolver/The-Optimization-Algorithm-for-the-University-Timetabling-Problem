from dataclasses import dataclass
from typing import List, Union

from data_input.basic_structure_loader.basic_structure_loader_utils.input_types import \
    TRList, TRList2, NorList
from time_ import Time, TimeRange
from utils.types_ import Day


@dataclass
class PrefTime:
    time_range: Union[TimeRange, None]
    points: int

    def to_generate(self) -> List:
        tr_list = self._get_tr_list()
        list_ = [tr_list, self.points]
        return list_

    def _get_tr_list(self):
        if self.time_range is None:
            tr_list = None
        else:
            tr_list = self.time_range.to_generate()
        return tr_list


class TimeLoader:
    def load_pref_times(self, day_time_list) -> List[PrefTime]:
        pref_times = []
        for pref_time_data in day_time_list:
            pref_time = self._get_pref_time(pref_time_data)
            pref_times.append(pref_time)
        self._assert_ranges_not_overlap(pref_times)
        return pref_times

    def load_times(self, avail: NorList, unavail: NorList) -> TRList2:
        avail_times = self._get_ranges(avail)
        unavail_times = self._get_ranges(unavail)
        self._assert_aval_ranges_correct(avail_times, unavail_times)
        return avail_times, unavail_times

    def _get_ranges(self, times_data) -> TRList:
        if times_data is None:
            return None
        time_ranges = []
        for time_data in times_data:
            t_r = self._get_range(time_data)
            time_ranges.append(t_r)
        return time_ranges

    def _get_pref_time(self, pref_time_data):
        match pref_time_data:
            case None, points:
                return PrefTime(None, points)
            case day_time, points:
                range_ = self._get_range(day_time)
                pref_time = PrefTime(range_, points)
                return pref_time
            case None, :
                return PrefTime(None, 0)

    @staticmethod
    def _get_range(day_time):
        match day_time:
            case day, s_t, e_t:
                range_ = TimeRange(Time(*s_t), Time(*e_t), day=Day(day-1))
                return range_
            case None:
                return None
            case _:
                raise ValueError(f"Incorrect TimeRange input data: {day_time}")

    def _assert_ranges_not_overlap(self,
                                   ranges: List[Union[TimeRange, PrefTime]]):
        raise NotImplementedError
        # todo do this after WeakSchedule

    @staticmethod
    def _assert_one_none(a, b):
        assert (a and b) != (b or a)

    def _assert_aval_ranges_correct(self, avail_times, unavail_times):
        self._assert_one_none(avail_times, unavail_times)
        self._assert_ranges_not_overlap(avail_times or unavail_times)

