import numpy as np
from PIL import Image as pim
from config import Config
from modules.wrapper import Wrapper


class Image:
    def __init__(self, path):
        self.pixels = np.asarray(pim.open(path))

    def width(self):
        return self.pixels.shape[1]

    def height(self):
        return self.pixels.shape[0]

    def save(self, wrapper: Wrapper, image_path, path_elements=None):
        image = np.empty(self.pixels.shape, dtype=np.uint8)
        elements = wrapper.elements()

        for index, element in enumerate(elements):
            box = element
            path_element = index

            if wrapper.is_qtree():
                box = element.box
                path_element = element

            x, y, w, h, state = box.x, box.y, box.w, box.h, box.state
            inner_color = state.color
            border_color = Config.Color.BORDER

            if path_elements is not None and path_element in path_elements:
                inner_color = Config.Color.PATH

            image[y:y + h - 1, x:x + w - 1, :] = inner_color
            image[y:y + h, x + w - 1, :] = border_color
            image[y + h - 1, x:x + w, :] = border_color

        pim.fromarray(image).save(image_path)
