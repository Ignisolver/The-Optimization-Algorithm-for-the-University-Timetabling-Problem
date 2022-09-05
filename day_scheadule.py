from typing import Iterator


class DaySchedule:
    def __init__(self, day_number):
        self.day_number = day_number
        self._classes = []

    def __repr__(self):
        pass

    def __add__(self, other):
        pass

    def __len__(self) -> int:
        """
        return time of classes in minutes
        """
        pass

    def __iter__(self) -> Iterator:
        return iter(self._classes)

    def get_classes(self):
        return self._classes

    def get_free_time(self):
        pass

    def get_brake_time(self):
        pass

    def get_brake_time_without_time_to_move(self):
        pass

    def get_last_classes_info(self):
        pass

    def get_first_classes_info(self):
        pass

    def get_amount_of_exercises(self):
        pass

    def get_amount_of_lectures(self):
        pass

    def assign_temporary(self):
        pass

    def revert_temporary_assign(self):
        pass

    def assign_classes(self):
        pass

    def pretty_represent(self):
        pass



