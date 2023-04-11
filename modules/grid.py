import numpy as np
from config import Config
from modules.box import Box
from modules.data import Data


class Grid(Data):
    def __init__(self, pixels: np.ndarray):
        super().__init__(pixels)
        self.rows = pixels.shape[0] // Config.Grid.MIN_SIZE
        self.columns = pixels.shape[1] // Config.Grid.MIN_SIZE
        self.boxes_list: list[Box] = []
        self.__init_boxes()

    def get(self, x, y):
        row = y // Config.Grid.MIN_SIZE
        column = x // Config.Grid.MIN_SIZE
        return self.index(row, column)

    def index(self, row, column):
        return row * self.columns + column

    def elements(self):
        return self.boxes_list

    def boxes(self, target_list=None):
        if target_list is None:
            return self.boxes_list

        boxes = []

        for target in target_list:
            boxes.append(self.boxes_list[target])

        return boxes

    def neighbour(self, index, direction: Data.Direction):
        row = index // self.columns
        column = index - row * self.columns

        if Config.Path.ALLOW_DIAGONAL and direction.is_diagonal():
            return self.__diagonal_neighbour(row, column, direction)

        return self.__cardinal_neighbour(row, column, direction)

    def neighbours(self, index):
        neighbours = []

        for direction in Data.Direction:
            neighbour = self.neighbour(index, direction)

            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def cost(self, start: int, end: int):
        return self.distance.get(self.boxes_list[start].center(), self.boxes_list[end].center())

    def heuristic(self, start: int, end: int):
        return self.cost(start, end)

    def __cardinal_neighbour(self, row, column, direction: Data.Direction):
        match direction:
            case Data.Direction.N:
                index = self.index(row - 1, column)
                if row > 0 and Data.check(self.boxes_list[index]):
                    return index
            case Data.Direction.E:
                index = self.index(row, column + 1)
                if column < self.columns - 1 and Data.check(self.boxes_list[index]):
                    return index
            case Data.Direction.S:
                index = self.index(row + 1, column)
                if row < self.rows - 1 and Data.check(self.boxes_list[index]):
                    return index
            case Data.Direction.W:
                index = self.index(row, column - 1)
                if column > 0 and Data.check(self.boxes_list[index]):
                    return index

    def __diagonal_neighbour(self, row, column, direction: Data.Direction):
        match direction:
            case Data.Direction.NW:
                index = self.index(row - 1, column - 1)
                if row > 0 and column > 0 and Data.check(self.boxes_list[index]):
                    return index
            case Data.Direction.NE:
                index = self.index(row - 1, column + 1)
                if row > 0 and column < self.columns - 1 and Data.check(self.boxes_list[index]):
                    return index
            case Data.Direction.SE:
                index = self.index(row + 1, column + 1)
                if row < self.rows - 1 and column < self.columns - 1 and Data.check(self.boxes_list[index]):
                    return index
            case Data.Direction.SW:
                index = self.index(row + 1, column - 1)
                if row < self.rows - 1 and column > 0 and Data.check(self.boxes_list[index]):
                    return index

    def __init_boxes(self):
        size = Config.Grid.MIN_SIZE

        assert self.pixels.shape[0] % size == 0 and self.pixels.shape[1] % size == 0, 'Invalid size'

        for row in range(self.rows):
            for column in range(self.columns):
                x = column * size
                y = row * size

                pixels_slice = self.pixels[y:y+size, x:x+size]
                state = Box.slice_state(pixels_slice)

                box = Box(x, y, size, size, state)
                self.boxes_list.append(box)
