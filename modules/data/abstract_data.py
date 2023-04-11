import math
import numpy as np
from modules.box import Box
from enum import IntEnum
from abc import ABC, abstractmethod


class AbstractData(ABC):

    class Direction(IntEnum):
        N = 0
        E = 1
        S = 2
        W = 3
        NW = 4
        NE = 5
        SE = 6
        SW = 7

        def is_diagonal(self):
            return (self == AbstractData.Direction.NW or
                    self == AbstractData.Direction.NE or
                    self == AbstractData.Direction.SE or
                    self == AbstractData.Direction.SW)

    class DistanceAlgorithm(IntEnum):
        EUCLIDIAN = 0
        MANHATTAN = 1

    def __init__(self, pixels: np.ndarray):
        self.pixels = pixels
        self.distance_algorithm = AbstractData.DistanceAlgorithm.EUCLIDIAN

    @staticmethod
    def check(box: Box):
        return box.state == Box.State.SAFE

    def distance(self, start, end):
        x = start[0] - end[0]
        y = start[1] - end[1]

        match self.distance_algorithm:
            case AbstractData.DistanceAlgorithm.EUCLIDIAN:
                return math.sqrt(x ** 2 + y ** 2)
            case AbstractData.DistanceAlgorithm.MANHATTAN:
                return abs(x) + abs(y)

    @classmethod
    @abstractmethod
    def get(cls, x: int, y: int):
        ...

    @classmethod
    @abstractmethod
    def elements(cls, *args, **kwargs):
        ...

    @classmethod
    @abstractmethod
    def boxes(cls, target_list=None):
        ...

    @classmethod
    @abstractmethod
    def neighbour(cls, element, direction: Direction):
        ...

    @classmethod
    @abstractmethod
    def neighbours(cls, *args, **kwargs):
        ...

    @classmethod
    @abstractmethod
    def cost(cls, start, end):
        ...

    @classmethod
    @abstractmethod
    def heuristic(cls, start, end):
        ...
