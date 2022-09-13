from typing import List, Union, Tuple

from data_input.basic_structures_loader import PreferredTime
from data_input.input_types import Tag, InputStructureType
from time_ import Time, TimeRange
from utils.types_ import Day


class BasicStructureLoaderPrimitive:
    @staticmethod
    def _assert_type(type_to_check: InputStructureType, correct_type: InputStructureType):
        assert type_to_check == correct_type

    @staticmethod
    def _assert_positive_int(value):
        assert isinstance(value, int)
        assert value >= 0

    @staticmethod
    def _assert_name_correct(name):
        assert isinstance(name, str)

    def _assert_correct_ids_tuple(self, tuple_):
        id_set = set()
        for id_ in tuple_:
            self._assert_positive_int(id_)
            id_set.add(id_)
        assert len(id_set) == len(tuple_)

    def _load_id_and_name(self, data: dict, correct_type) -> Tuple[int, str]:
        type_ = InputStructureType(data[Tag.TYPE])
        self._assert_type(type_, correct_type)

        id_ = data[Tag.ID]
        self._assert_positive_int(id_)

        name = data[Tag.NAME]
        self._assert_name_correct(name)
        return id_, name


class PrimitiveTimeLoader:
    @staticmethod
    def _unpack_time_ranges_from_time(time: tuple):
        days, (start_h, start_m), (end_h, end_m) = time
        time_ranges = []
        for day in days:
            day -= 1
            start = Time(start_h, end_h)
            end = Time(end_h, end_m)
            time_ranges.append(TimeRange(start, end, day=Day(day)))
        return time_ranges

    def _extract_times_from_list(self, times: list) -> List[TimeRange]:
        extracted_times = []
        for time in times:
            time_range = self._unpack_time_ranges_from_time(time)
            extracted_times.extend(time_range)
        return extracted_times

    def _assert_times_do_not_overlap(self, times):
        raise NotImplementedError

    def _assert_times_correctness(self, raw_available_times_list, raw_unavailable_times_list):
        assert (raw_available_times_list is None) and (raw_unavailable_times_list is None)
        assert (raw_available_times_list is not None) and (raw_unavailable_times_list is not None)
        self._assert_times_do_not_overlap(raw_available_times_list or raw_unavailable_times_list)

    def _extract_times_or_none(self, times) -> Union[List[TimeRange], None]:
        if times is None:
            return None
        else:
            extracted_times = self._extract_times_from_list(times)
            return extracted_times

    def load_preferred_times(self, raw_time_and_point_list) -> Union[None, List[PreferredTime]]:
        if raw_time_and_point_list is None:
            return None
        else:
            preferred_times = []
            for raw_times_and_points in raw_time_and_point_list:
                raw_times, points = raw_times_and_points
                time_ranges = self._unpack_time_ranges_from_time(raw_times)
                for time_range in time_ranges:
                    preferred_times.append(PreferredTime(time_range, points))
            return preferred_times

    def load_available_and_unavailable_times(self, data):
        available_times = self._extract_times_or_none(data[Tag.AVAILABLE_TIMES])

        unavailable_times = self._extract_times_or_none(data[Tag.UNAVAILABLE_TIMES])

        self._assert_times_correctness(available_times, unavailable_times)
        return available_times, unavailable_times
