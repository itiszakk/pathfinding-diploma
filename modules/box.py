import numpy as np
from enum import Enum
from config import Config


class Box:

    class State(Enum):
        def __init__(self, index, color):
            self.index = index
            self.color = color

        EMPTY = 0, Config.Color.WHITE
        INTERMEDIATE = 1, Config.Color.LIGHTGRAY
        BLOCKED = 2, Config.Color.BLACK

        @staticmethod
        def slice_state(data_slice: np.ndarray):
            any_white = np.any(data_slice == Config.Color.WHITE)
            any_black = np.any(data_slice == Config.Color.BLACK)

            if any_white and not any_black:
                return Box.State.EMPTY

            if not any_white and any_black:
                return Box.State.BLOCKED

            return Box.State.INTERMEDIATE

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