import numpy as np
from PIL import Image as pim
from PIL import ImageDraw

from config import Config
from modules.wrapper import Wrapper


class Image:
    def __init__(self, path):
        self.pixels = np.asarray(pim.open(path))

    def width(self):
        return self.pixels.shape[1]

    def height(self):
        return self.pixels.shape[0]

    def save(self, wrapper: Wrapper, image_path, path=None, visited=None):
        image = np.full(self.pixels.shape, Config.Color.BACKGROUND, dtype=np.uint8)
        elements = wrapper.elements()

        for index, element in enumerate(elements):
            box = element
            path_element = index

            if wrapper.is_qtree():
                box = element.box
                path_element = element

            color = box.state.color
            border = Config.Image.BORDER

            if visited is not None and path_element in visited:
                color = Config.Color.VISITED

            if path is not None and path_element in path:
                color = Config.Color.PATH

            image[box.y:box.y + box.h - border, box.x:box.x + box.w - border, :] = color

        image = pim.fromarray(image)

        if path is not None:
            Image.__draw_trajectory(wrapper, image, path)

        image.save(image_path)

    @staticmethod
    def __draw_trajectory(wrapper, image, path):
        image_draw = ImageDraw.Draw(image)
        length = len(path) - 1

        for i, element in enumerate(path):
            if i == length:
                break

            center = None
            next_center = None

            if wrapper.is_grid():
                center = wrapper.data.element(element).center()
                next_center = wrapper.data.element(path[i + 1]).center()
            elif wrapper.is_qtree():
                center = element.box.center()
                next_center = path[i + 1].box.center()

            x0, y0 = center
            x1, y1 = next_center
            border = Config.Image.BORDER

            image_draw.line((x0 - border, y0 - border, x1 - border, y1 - border),
                            fill=Config.Color.TRAJECTORY, width=Config.Image.TRAJECTORY)
