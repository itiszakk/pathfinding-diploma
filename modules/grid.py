import numpy as np
from PIL import Image
from config import Config
from modules.box import Box
from modules.common import Direction


class Grid:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.rows = image.shape[0] // Config.Grid.MIN_SIZE
        self.columns = image.shape[1] // Config.Grid.MIN_SIZE
        self.elements: list[list[Box]] = []
        self.__init_elements()

    def save_image(self, image_path, path=None):
        image = np.empty(shape=(self.image.shape[0], self.image.shape[1], 3), dtype=np.uint8)

        for row, row_elements in enumerate(self.elements):
            for column, box in enumerate(row_elements):
                index = row, column
                color = Config.Color.GREEN if path is not None and index in path else box.state.color
                image[box.y:box.y + box.h - 1, box.x:box.x + box.w - 1, :] = color
                image[box.y:box.y + box.h, box.x + box.w - 1, :] = Config.Color.DARKGRAY
                image[box.y + box.h - 1, box.x:box.x + box.w] = Config.Color.DARKGRAY

        image = Image.fromarray(image)
        image.save(image_path)

    def get(self, x, y):
        return y // Config.Grid.MIN_SIZE, x // Config.Grid.MIN_SIZE

    def neighbours(self, index, check):
        neighbours = []

        for direction in Direction:
            neighbour = self.__get_neighbour_by_direction(index, direction, check)

            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def __get_neighbour_by_direction(self, index, direction: Direction, check):
        row, column = index

        if direction == Direction.N:
            if row > 0 and check(self.elements[row - 1][column]):
                return row - 1, column

        if direction == Direction.E:
            if column < self.columns - 1 and check(self.elements[row][column + 1]):
                return row, column + 1

        if direction == Direction.S:
            if row < self.rows - 1 and check(self.elements[row + 1][column]):
                return row + 1, column

        if direction == Direction.W:
            if column > 0 and check(self.elements[row][column - 1]):
                return row, column - 1

    def print_info(self):
        for element in self.elements:
            print(element)

        print(f'Elements: {len(self.elements)}')

    def __init_elements(self):
        size = Config.Grid.MIN_SIZE

        assert self.image.shape[0] % size == 0 and self.image.shape[1] % size == 0, 'Invalid size'

        for row in range(self.rows):
            row_elements = []

            for column in range(self.columns):
                x = column * size
                y = row * size

                image_slice = self.image[y:y+size, x:x+size]
                state = Box.State.slice_state(image_slice)

                box = Box(x, y, size, size, state)
                row_elements.append(box)

            self.elements.append(row_elements)
