from typing import List, Union

from data_input.basic_structure_loader.basic_structure_loader_utils. \
    input_types import Tag, DaysTimeT, DaysTimeListT, PrefDaysTimeListT
from time_ import Time, TimeRange
from utils.types_ import Day


class PreferredTime:
    def __init__(self, day_time_points):
        match day_time_points:
            case None, points:
                self.time_range = None
                self.points = points
            case day, (s_h, s_m), (e_h, e_m), points:
                self.time_range = TimeRange(Time(s_h, s_m),
                                            Time(e_h, e_m),
                                            day=day)
                self.points = points
            case _:
                raise ValueError(f"Incorrect PrefferedTime "
                                 f"input: {day_time_points}")


class TimeLoader:
    @staticmethod
    def _create_ranges(time: DaysTimeT) -> List[TimeRange]:
        days, (s_h, s_m), (e_h, e_m) = time
        ranges = []
        for day in days:
            day -= 1
            start = Time(s_h, s_m)
            end = Time(e_h, e_m)
            ranges.append(TimeRange(start, end, day=Day(day)))
        return ranges

    def _extract_ranges(self, times: DaysTimeListT) -> List[TimeRange]:
        ranges = []
        for time in times:
            ext_ranges = self._create_ranges(time)
            ranges.extend(ext_ranges)
        return ranges

    def _assert_ranges_not_overlap(self, times: List[TimeRange]):
        raise NotImplementedError
        # todo do this after WeakSchedule

    @staticmethod
    def _assert_both_none(one, another):
        assert (one is None) and (another is None)

    @staticmethod
    def _assert_both_not_none(one, another):
        assert (one is not None) and (another is not None)

    def _assert_ranges_correct(self, avail_times, unavail_times):
        self._assert_both_none(avail_times, unavail_times)
        self._assert_both_not_none(avail_times, unavail_times)
        self._assert_ranges_not_overlap(avail_times or unavail_times)

    def _get_ranges_or_none(self, times) -> Union[List[TimeRange], None]:
        if times is None:
            return None
        else:
            day_time_list = self._extract_time_for_each_day(times)

            return ext_times

    @staticmethod
    def _extract_days(days_rest):
        day_rest_list = []
        for days_and_times in days_rest:
            days, *rest = days_and_times
            for day in days:
                day_rest_list.append([day, rest])
        return day_rest_list


    @staticmethod
    def create_pref_times(day_time_points_list) -> List[PreferredTime]:
        pref_times = []
        for day_time_points in day_time_points_list:
            pref_times.append(PreferredTime(day_time_points))
        return pref_times

    def load_pref_times(self,
                        days_time_points_list: PrefDaysTimeListT,
                        ) -> Union[None, List[PreferredTime]]:
        if days_time_points_list is None:
            return [PreferredTime(None, 0)]
        else:
            pref_times = self.create_pref_times(days_time_points_list)
            return pref_times

    def load_available_and_unavailable_times(self, data: dict):
        avail_times = self._get_ranges_or_none(data[Tag.AVAILABLE_TIMES])
        unavail_times = self._get_ranges_or_none(data[Tag.UNAVAILABLE_TIMES])
        self._assert_ranges_correct(avail_times, unavail_times)
        return avail_times, unavail_times

# todo do this again - split for days, time_range_from_list, pref_time_from_tr_and_points
