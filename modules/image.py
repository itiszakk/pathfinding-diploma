import itertools

import numpy as np
from PIL import Image as im
from PIL import ImageDraw as imdraw

from config import Config
from modules.data.abstract_data import AbstractData
from modules.pathfinder.pathfinder_info import PathfinderInfo


class Image:
    def __init__(self, path):
        image = im.open(path).convert('RGB')
        self.pixels = np.asarray(image)

    def width(self):
        return self.pixels.shape[1]

    def height(self):
        return self.pixels.shape[0]

    def save(self, data: AbstractData, image_path, info: PathfinderInfo | None = None):
        image = im.new('RGB', (self.pixels.shape[1], self.pixels.shape[0]))
        image_draw = imdraw.Draw(image)

        self.__draw_boxes(image_draw, data, info)

        if info is not None:
            self.__draw_trajectory(image_draw, info)

        image.save(image_path)

    def __draw_boxes(self, image_draw, data: AbstractData, info: PathfinderInfo | None = None):
        boxes = data.boxes()

        for box in boxes:
            color = info.get_box_color(box) if info is not None else box.state.color
            border = Config.Image.BORDER

            x0, y0 = box.x, box.y
            x1, y1 = box.x + box.w - 1, box.y + box.h - 1

            image_draw.rectangle((x0, y0, x1, y1), fill=color, outline=Config.Color.BORDER, width=border)

    def __draw_trajectory(self, image_draw, info: PathfinderInfo):
        for current_point, next_point in itertools.pairwise(info.points):
            self.__draw_line(image_draw, current_point, next_point)

    def __draw_line(self, image_draw, p0, p1):
        x0, y0 = p0
        x1, y1 = p1

        image_draw.line((x0, y0, x1, y1), fill=Config.Color.TRAJECTORY, width=Config.Image.TRAJECTORY)

