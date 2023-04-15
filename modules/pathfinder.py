import itertools
from abc import ABC, abstractmethod

from pqdict import pqdict
from shapely.geometry import LineString

from config import Config
from modules.data import AbstractData, Grid
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

        self.__set_trajectory_points()

        if Config.Path.ENABLE_SMOOTHING:
            self.__smooth_trajectory()

    def set_visited(self, data, visited):
        if visited is None:
            return

        self.visited = visited
        self.visited_boxes = data.boxes(visited)

    def __set_trajectory_points(self):
        self.points = [self.end]

        for box in self.path_boxes[1:-1]:
            self.points.append(box.center())

        self.points.append(self.start)

    def __smooth_trajectory(self):
        smooth_trajectory = [self.end]

        for index, trajectory in enumerate(itertools.pairwise(self.points)):
            box = self.path_boxes[index]

            n_line = (box.x, box.y), (box.x + box.w - 1, box.y)
            e_line = (box.x + box.w - 1, box.y), (box.x + box.w - 1, box.y + box.h - 1)
            s_line = (box.x, box.y + box.h - 1), (box.x + box.w - 1, box.y + box.h - 1)
            w_line = (box.x, box.y), (box.x, box.y + box.h - 1)

            box_segments = [n_line, e_line, s_line, w_line]

            for box_segment in box_segments:
                intersection = self.__line_intersection(trajectory, box_segment)

                if intersection is not None:
                    smooth_trajectory.append(intersection)
                    break

        smooth_trajectory.append(self.start)
        self.points = smooth_trajectory

    def __line_intersection(self, l0, l1):
        l0 = LineString(l0)
        l1 = LineString(l1)

        if not l0.intersects(l1):
            return None

        intersection = l0.intersection(l1)

        return round(intersection.x), round(intersection.y)


class AbstractPathfinder(ABC):
    def __init__(self, pathfinder_name, data: AbstractData, start, end):
        self.data = data
        self.start = data.get(*start)
        self.end = data.get(*end)
        self.info = PathfinderInfo(pathfinder_name, start, end)

    @classmethod
    @abstractmethod
    def search(cls):
        ...

    def build_info(self, visited) -> PathfinderInfo:
        self.info.set_visited(self.data, list(visited.keys()))

        if self.end not in visited:
            return self.info

        path = self.__build_path(visited)
        self.info.set_path(self.data, path)
        return self.info

    def __build_path(self, visited):
        path = []
        current = self.end

        while current in visited:
            path.append(current)
            current = visited[current]

        return path


class AStar(AbstractPathfinder):
    def __init__(self, data: AbstractData, start, end):
        super().__init__(type(self).__name__, data, start, end)

    def search(self):
        priority_queue = pqdict({self.start: 0})
        cost_so_far = {self.start: 0}
        visited = {self.start: None}

        while priority_queue:
            current = priority_queue.popitem()[0]

            if current == self.end:
                break

            neighbours = self.data.neighbours(current)

            for neighbour in neighbours:
                cost = cost_so_far[current] + self.data.cost(current, neighbour)

                if neighbour not in visited or cost < cost_so_far[neighbour]:
                    priority_queue[neighbour] = cost + self.data.heuristic(neighbour, self.end)
                    cost_so_far[neighbour] = cost
                    visited[neighbour] = current

        return self.build_info(visited)


class JPS(AbstractPathfinder):
    def __init__(self, data: Grid, start, end):
        super().__init__(type(self).__name__, data, start, end)
        assert isinstance(data, Grid)

    def search(self):
        pass
