import itertools

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

    def save(self, data: AbstractData, image_path, start=None, end=None, path=None, visited=None):
        image = im.new('RGB', (self.pixels.shape[1], self.pixels.shape[0]))
        image_draw = imdraw.Draw(image)

        boxes = data.boxes()
        path_boxes = data.boxes(path) if path is not None else None
        visited_boxes = data.boxes(visited) if visited is not None else None

        has_waypoints = start is not None and end is not None
        has_trajectory = path_boxes is not None and len(path_boxes)

        self.__draw_boxes(image_draw, boxes, path_boxes, visited_boxes)

        if has_waypoints and has_trajectory and Config.Image.TRAJECTORY:
            points = self.__get_path_points(start, end, path_boxes)
            self.__draw_trajectory(image_draw, points)

        image.save(image_path)

    def __get_path_points(self, start, end, path_boxes):
        points = [end]

        for box in path_boxes[1:-1]:
            points.append(box.center())

        points.append(start)

        return points

    def __draw_boxes(self, image_draw, boxes, path_boxes=None, visited_boxes=None):
        for box in boxes:
            color = box.state.color
            border = Config.Image.BORDER

            if visited_boxes is not None and box in visited_boxes:
                color = Config.Color.VISITED

            if path_boxes is not None and box in path_boxes:
                color = Config.Color.PATH

            x0, y0 = box.x, box.y
            x1, y1 = box.x + box.w - 1, box.y + box.h - 1

            image_draw.rectangle((x0, y0, x1, y1), fill=color, outline=Config.Color.BORDER, width=border)

    def __draw_trajectory(self, image_draw, points):
        for current_point, next_point in itertools.pairwise(points):
            self.__draw_line(image_draw, current_point, next_point)

    def __draw_line(self, image_draw, p0, p1):
        x0, y0 = p0
        x1, y1 = p1

        image_draw.line((x0, y0, x1, y1), fill=Config.Color.TRAJECTORY, width=Config.Image.TRAJECTORY)

