import math


class Distance:

    @staticmethod
    def euclidian(p0, p1):
        x0, y0 = p0
        x1, y1 = p1

        return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

    @staticmethod
    def manhattan(p0, p1):
        x0, y0 = p0
        x1, y1 = p1

        return abs(x0 - x1) + abs(y0 - y1)

