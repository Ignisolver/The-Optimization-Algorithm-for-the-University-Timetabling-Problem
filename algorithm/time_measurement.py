from time import time


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        end = time()
        elapsed_time = round(end-start, 2)
        mins = int(elapsed_time // 60)
        sec = elapsed_time % 60
        print(30 * "-")
        print(f"ELAPSED TIME: {mins} min {round(sec, 2)} sec")
        return res
    return wrapper
