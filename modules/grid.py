import numpy as np
from config import Config
from modules.box import Box, Direction


class Grid:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.rows = image.shape[0] // Config.Grid.MIN_SIZE
        self.columns = image.shape[1] // Config.Grid.MIN_SIZE
        self.elements: list[Box] = []
        self.__init_elements()

    def index(self, i, j):
        return i * self.columns + j

    def element(self, i, j):
        return self.elements[self.index(i, j)]

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
            if row > 0 and check(self.element(row - 1, column)):
                return self.index(row - 1, column)

        if direction == Direction.E:
            if column < self.columns - 1 and check(self.element(row, column + 1)):
                return self.index(row, column + 1)

        if direction == Direction.S:
            if row < self.rows - 1 and check(self.element(row + 1, column)):
                return self.index(row + 1, column)

        if direction == Direction.W:
            if column > 0 and check(self.element(row, column - 1)):
                return self.index(row, column - 1)

    def print_info(self):
        for element in self.elements:
            print(element)

        print(f'Elements: {len(self.elements)}')

    def __init_elements(self):
        size = Config.Grid.MIN_SIZE

        assert self.image.shape[0] % size == 0 and self.image.shape[1] % size == 0, 'Invalid size'

        for row in range(self.rows):
            for column in range(self.columns):
                x = column * size
                y = row * size

                image_slice = self.image[y:y+size, x:x+size]
                state = Box.slice_state(image_slice)

                box = Box(x, y, size, size, state)
                self.elements.append(box)
