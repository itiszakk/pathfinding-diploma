import time


def now():
    return int(time.time_ns() / 1_000_000)
