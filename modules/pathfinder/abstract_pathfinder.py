from abc import ABC, abstractmethod

from modules.data.abstract_data import AbstractData
from modules.pathfinder.pathfinder_info import PathfinderInfo


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

