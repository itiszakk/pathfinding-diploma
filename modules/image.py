import numpy as np
from PIL import Image as im
from PIL import ImageDraw as imdraw

from config import Config
from modules.data.abstract_data import AbstractData


class Image:
    def __init__(self, path):
        image = im.open(path).convert('RGB')
        self.pixels = np.asarray(image)

    def width(self):
        return self.pixels.shape[1]

    def height(self):
        return self.pixels.shape[0]

    def save(self, data: AbstractData, image_path, path=None, visited=None):
        image = im.new('RGB', (self.pixels.shape[1], self.pixels.shape[0]))
        image_draw = imdraw.Draw(image)

        boxes = data.boxes()
        path_boxes = data.boxes(path) if path is not None else None
        visited_boxes = data.boxes(visited) if visited is not None else None

        self.__draw_boxes(image_draw, boxes, path_boxes, visited_boxes)

        if path_boxes is not None and Config.Image.TRAJECTORY:
            self.__draw_trajectory(image_draw, path_boxes)

        image.save(image_path)

    def __draw_boxes(self, image_draw, boxes, path_boxes=None, visited_boxes=None):
        for box in boxes:
            color = box.state.color
            border = Config.Image.BORDER

            if path_boxes is not None and box in visited_boxes:
                color = Config.Color.VISITED

            if visited_boxes is not None and box in path_boxes:
                color = Config.Color.PATH

            image_draw.rectangle((box.x, box.y, box.x + box.w - 1, box.y + box.h - 1),
                                 fill=color, outline=Config.Color.BORDER, width=border)

    def __draw_trajectory(self, image_draw, path_boxes):
        for index in range(len(path_boxes) - 1):
            x0, y0 = path_boxes[index].center()
            x1, y1 = path_boxes[index + 1].center()

            image_draw.line((x0, y0, x1, y1), fill=Config.Color.TRAJECTORY, width=Config.Image.TRAJECTORY)
