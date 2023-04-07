import time
from enum import IntEnum


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class Utils:

    @staticmethod
    def time_ms():
        return int(round(time.time() * 1000))
