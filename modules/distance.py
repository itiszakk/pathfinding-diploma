import math
from enum import IntEnum


class Distance:

    class Algorithm(IntEnum):
        EUCLIDIAN = 0
        MANHATTAN = 1

    def __init__(self):
        self.algorithm = Distance.Algorithm.EUCLIDIAN

    def get(self, x, y):
        if self.algorithm == Distance.Algorithm.EUCLIDIAN:
            return math.sqrt(x ** 2 + y ** 2)

        if self.algorithm == Distance.Algorithm.MANHATTAN:
            return x + y