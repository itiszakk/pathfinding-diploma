import numpy as np

from config import Config
from modules.box import Box, Direction


class Grid:
    def __init__(self, pixels: np.ndarray):
        self.pixels = pixels
        self.rows = pixels.shape[0] // Config.Grid.MIN_SIZE
        self.columns = pixels.shape[1] // Config.Grid.MIN_SIZE
        self.elements: list[Box] = []
        self.__init_elements()

    def index(self, i, j):
        return i * self.columns + j

    def element(self, index: int | tuple[int, int]):
        if isinstance(index, int):
            return self.elements[index]
        elif isinstance(index, tuple):
            return self.elements[self.index(*index)]

    def get(self, x, y):
        row = y // Config.Grid.MIN_SIZE
        column = x // Config.Grid.MIN_SIZE
        return self.index(row, column)

    def neighbours(self, index, check):
        neighbours = []

        for direction in Direction:
            neighbour = self.__get_neighbour_by_direction(index, direction, check)

            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def __get_neighbour_by_direction(self, index, direction: Direction, check):
        row = index // self.columns
        column = index - row * self.columns

        if direction == Direction.N:
            if row > 0 and check(self.element((row - 1, column))):
                return self.index(row - 1, column)
        elif direction == Direction.E:
            if column < self.columns - 1 and check(self.element((row, column + 1))):
                return self.index(row, column + 1)
        elif direction == Direction.S:
            if row < self.rows - 1 and check(self.element((row + 1, column))):
                return self.index(row + 1, column)
        elif direction == Direction.W:
            if column > 0 and check(self.element((row, column - 1))):
                return self.index(row, column - 1)
        elif direction == Direction.NW:
            if row > 0 and column > 0 and check(self.element((row - 1, column - 1))):
                return self.index(row - 1, column - 1)
        elif direction == Direction.NE:
            if row > 0 and column < self.columns - 1 and check(self.element((row - 1, column + 1))):
                return self.index(row - 1, column + 1)
        elif direction == Direction.SE:
            if row < self.rows - 1 and column < self.columns - 1 and check(self.element((row + 1, column + 1))):
                return self.index(row + 1, column + 1)
        elif direction == Direction.SW:
            if row < self.rows - 1 and column > 0 and check(self.element((row + 1, column - 1))):
                return self.index(row + 1, column - 1)

    def print_info(self):
        for element in self.elements:
            print(element)

        print(f'Elements: {len(self.elements)}')

    def __init_elements(self):
        size = Config.Grid.MIN_SIZE

        assert self.pixels.shape[0] % size == 0 and self.pixels.shape[1] % size == 0, 'Invalid size'

        for row in range(self.rows):
            for column in range(self.columns):
                x = column * size
                y = row * size

                pixels_slice = self.pixels[y:y+size, x:x+size]
                state = Box.slice_state(pixels_slice)

                box = Box(x, y, size, size, state)
                self.elements.append(box)
