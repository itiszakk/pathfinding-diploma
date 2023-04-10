from collections import deque
from enum import IntEnum

from pqdict import pqdict

from modules.utils import timeit
from modules.data import Data


class Pathfinder:

    class Algorithm(IntEnum):
        BFS = 0
        ASTAR = 1
        JPS = 2

    def __init__(self, data: Data, start, end):
        self.data = data
        self.start = data.get(*start)
        self.end = data.get(*end)
        self.algorithm = Pathfinder.Algorithm.BFS

    @timeit
    def execute(self):
        algorithms = [self.__bfs, self.__astar, self.__jps]
        return algorithms[self.algorithm]()

    def __build_path(self, visited):
        path = []
        current = self.end

        while current in visited:
            path.append(current)
            current = visited[current]

        return path

    def __bfs(self):
        queue = deque([self.start])
        visited = {self.start: None}

        while queue:
            current = queue.popleft()

            if current == self.end:
                break

            neighbours = self.data.neighbours(current)

            for neighbour in neighbours:
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited[neighbour] = current

        return self.__build_path(visited)

    def __astar(self):
        queue = pqdict({self.start: 0})
        visited = {self.start: None}
        costs = {self.start: 0}

        while queue:
            current, _ = queue.popitem()

            if current == self.end:
                break

            neighbours = self.data.neighbours(current)

            for neighbour in neighbours:
                cost = costs[current] + self.data.cost(current, neighbour)

                if neighbour not in costs or cost < costs[neighbour]:
                    costs[neighbour] = cost
                    queue[neighbour] = cost + self.data.heuristic(neighbour, self.end)
                    visited[neighbour] = current

        return self.__build_path(visited), list(costs.keys())

    def __jps(self):
        pass


