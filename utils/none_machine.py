class NoneMachine:
    @staticmethod
    def both_nones(a, b):
        return (a is None) and (b is None)

    @staticmethod
    def both_not_none(a, b):
        return (a is not None) and (b is not None)

    @staticmethod
    def count_nones(list_):
        return sum(1 for el in list_ if el is None)

    def contain_one_none(self, list_):
        return self.is_nones_amount(list_, 1)

    def is_nones_amount(self, list_, nones_amount):
        return self.count_nones(list_) == nones_amount


NM = NoneMachine()
