import numpy as np
from PIL import Image
from config import Config
from modules.box import Box


class Grid:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.elements: list[list[Box]] = []
        self.__init_elements()

    def save_image(self, path):
        image = np.empty(shape=self.image.shape, dtype=self.image.dtype)

        for row in self.elements:
            for box in row:
                inner_slice = image[box.y:box.y + box.h - 1, box.x:box.x + box.w - 1]
                inner_slice.fill(box.state.color)

                bottom_slice = image[box.y:box.y + box.h, box.x + box.w - 1]
                bottom_slice.fill(Config.Color.DARKGRAY)

                right_slice = image[box.y + box.h - 1, box.x:box.x + box.w]
                right_slice.fill(Config.Color.DARKGRAY)

        image = Image.fromarray(image)
        image.save(path)

    def get(self, x, y):
        i = y // Config.Grid.MIN_SIZE
        j = x // Config.Grid.MIN_SIZE
        return self.elements[i][j]

    def print_info(self):
        for element in self.elements:
            print(element)

        print(f'Elements: {len(self.elements)}')

    def __init_elements(self):
        size = Config.Grid.MIN_SIZE

        assert self.image.shape[0] % size == 0 and self.image.shape[1] % size == 0, 'Invalid size'

        rows = self.image.shape[0] // size
        columns = self.image.shape[1] // size

        for row in range(rows):
            row_elements = []

            for column in range(columns):
                x = column * size
                y = row * size

                image_slice = self.image[y:y+size, x:x+size]
                state = Box.State.slice_state(image_slice)

                box = Box(x, y, size, size, state)
                row_elements.append(box)

            self.elements.append(row_elements)
