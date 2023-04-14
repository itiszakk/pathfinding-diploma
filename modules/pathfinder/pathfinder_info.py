import itertools
import math

from config import Config

from modules.distance import Distance


class PathfinderInfo:
    def __init__(self, pathfinder_name, start, end):
        self.pathfinder_name = pathfinder_name
        self.start = start
        self.end = end
        self.path = None
        self.visited = None
        self.path_boxes = None
        self.visited_boxes = None
        self.points = None

    def trajectory_length(self):
        trajectory_length = 0

        for p0, p1 in itertools.pairwise(self.points):
            trajectory_length += Distance.euclidian(p0, p1)

        return trajectory_length

    def path_length(self):
        if self.path is None:
            return None

        return len(self.path)

    def visited_length(self):
        if self.visited is None:
            return None

        return len(self.visited)

    def set_path(self, data, path):
        if path is None:
            return

        self.path = path
        self.path_boxes = data.boxes(path)
        self.__set_points()

    def set_visited(self, data, visited):
        if visited is None:
            return

        self.visited = visited
        self.visited_boxes = data.boxes(visited)

    def get_box_color(self, box):
        is_path_box = self.path_boxes is not None and box in self.path_boxes
        is_visited_box = self.visited_boxes is not None and box in self.visited_boxes

        if is_path_box:
            return Config.Color.PATH

        if is_visited_box:
            return Config.Color.VISITED

        return box.state.color

    def __set_points(self):
        self.points = [self.end]

        for box in self.path_boxes[1:-1]:
            self.points.append(box.center())

        self.points.append(self.start)
