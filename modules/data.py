import numpy as np
from modules.box import Box
from modules.distance import Distance
from enum import IntEnum
from abc import ABC, abstractmethod


class Data(ABC):

    class Direction(IntEnum):
        N = 0
        E = 1
        S = 2
        W = 3
        NW = 4
        NE = 5
        SE = 6
        SW = 7

    def __init__(self, pixels: np.ndarray):
        self.pixels = pixels
        self.distance = Distance()

    @staticmethod
    def check(box: Box):
        return box.state == Box.State.SAFE

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
    def neighbour(cls, *args, **kwargs):
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
