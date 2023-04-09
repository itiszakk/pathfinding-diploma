import time
from collections import deque
from enum import IntEnum
from pqdict import pqdict
from modules.wrapper import Wrapper


def show_info(func):
    def wrapper(*args):
        start_time = int(round(time.time() * 1000))
        result = func(*args)
        end_time = int(round(time.time() * 1000)) - start_time

        print(args[0])
        print(f'Length: {len(result)}')
        print(f'Time: {end_time} ms\n')

        return result

    return wrapper


class Pathfinder:

    class Algorithm(IntEnum):
        BFS = 0
        ASTAR = 1
        JPS = 2

    def __init__(self, wrapper: Wrapper, start, end):
        self.wrapper = wrapper
        self.start = wrapper.data.get(*start)
        self.end = wrapper.data.get(*end)
        self.algorithm = Pathfinder.Algorithm.BFS

        # Wrapped functions
        self.neighbours = wrapper.neighbours_function()
        self.cost = wrapper.cost_function()
        self.heuristic = wrapper.heuristic_function()

    def __repr__(self):
        return (f'Wrapper: {type(self.wrapper.data).__name__}\n'
                f'Distance: {self.wrapper.distance.algorithm.name}\n'
                f'Algorithm: {self.algorithm.name}\n'
                f'Start: {self.start}\n'
                f'End: {self.end}')

    @show_info
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

            neighbours = self.neighbours(current)

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

            neighbours = self.neighbours(current)

            for neighbour in neighbours:
                cost = costs[current] + self.cost(current, neighbour)

                if neighbour not in costs or cost < costs[neighbour]:
                    queue[neighbour] = cost + self.heuristic(neighbour, self.end)
                    visited[neighbour] = current
                    costs[neighbour] = cost

        return self.__build_path(visited)

    def __jps(self):
        pass


