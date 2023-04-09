import math
from enum import IntEnum


class Distance:

    class Algorithm(IntEnum):
        EUCLIDIAN = 0
        MANHATTAN = 1

    def __init__(self):
        self.algorithm = Distance.Algorithm.EUCLIDIAN

    def get(self, start, end):
        start_x, start_y = start
        end_x, end_y = end

        x = abs(start_x - end_x)
        y = abs(start_y - end_y)

        if self.algorithm == Distance.Algorithm.EUCLIDIAN:
            return math.sqrt(x ** 2 + y ** 2)
        elif self.algorithm == Distance.Algorithm.MANHATTAN:
            return x + y
