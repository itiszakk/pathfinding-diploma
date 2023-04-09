import time


def time_ms():
    return int(round(time.time() * 1000))


def timeit(func):

    def wrapper(*args, **kwargs):
        start_time = time_ms()
        result = func(*args, **kwargs)
        end_time = time_ms() - start_time

        print(f'Time: {end_time} ms')

        return result

    return wrapper
