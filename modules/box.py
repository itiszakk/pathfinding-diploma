import numpy as np
from enum import Enum, IntEnum
from config import Config


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class Box:

    class State(Enum):
        def __init__(self, index, color):
            self.index = index
            self.color = color

        EMPTY = 0, Config.Color.EMPTY
        INTERMEDIATE = 1, Config.Color.INTERMEDIATE
        BLOCKED = 2, Config.Color.BLOCKED

    def __init__(self, x, y, w, h, state=State.EMPTY):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.state = state

    def __repr__(self):
        return f'Box(x={self.x}, y={self.y}, w={self.w}, h={self.h}, state={self.state})'

    def contains(self, x, y):
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    def center(self):
        return self.x + self.w // 2, self.y + self.h // 2

    @staticmethod
    def slice_state(data_slice: np.ndarray):
        any_empty = np.any(data_slice == Config.Color.EMPTY)
        any_blocked = np.any(data_slice == Config.Color.BLOCKED)

        if any_empty and not any_blocked:
            return Box.State.EMPTY

        if not any_empty and any_blocked:
            return Box.State.BLOCKED

        return Box.State.INTERMEDIATE
