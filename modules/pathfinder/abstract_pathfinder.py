from abc import ABC, abstractmethod

from modules.data.abstract_data import AbstractData


class AbstractPathfinder(ABC):
    def __init__(self, data: AbstractData, start, end):
        self.data = data
        self.start = data.get(*start)
        self.end = data.get(*end)

    @classmethod
    @abstractmethod
    def search(cls):
        ...

    def build_path(self, visited):
        if self.end not in visited:
            return None, list(visited.keys())

        path = []
        current = self.end

        while current in visited:
            path.append(current)
            current = visited[current]

        return path, list(visited.keys())
