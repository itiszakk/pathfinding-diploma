from enum import Enum
from collections import deque
from modules.box import Box
from modules.grid import Grid
from modules.qtree import QTree
from modules.utils import time_ms, is_grid, is_qtree


class Pathfinder:

    class Algorithm(Enum):
        def __init__(self, index, label):
            self.index = index
            self.label = label

        BFS = 0, 'Breadth-First Search'
        ASTAR = 1, 'A*'
        JPS = 2, 'Jump Point Search'

    def __init__(self, data: Grid | QTree, algorithm: Algorithm, start, end):
        self.data = data
        self.algorithm = algorithm
        self.start = data.get(*start)
        self.end = data.get(*end)

    def execute(self):
        methods = [self.__bfs, self.__astar, self.__jps]

        time = time_ms()
        path = methods[self.algorithm.index]()

        self.__print_info(len(path), time_ms() - time)

        return path

    def __print_info(self, path_length, time):
        print(f'\n'
              f'Algorithm: {self.algorithm.label}\n'
              f'Data type: {type(self.data).__name__}\n'
              f'From: {self.start}\n'
              f'To: {self.end}\n'
              f'Path length: {path_length}\n'
              f'Time: {time} ms')

    def check_wrapper(self):

        def grid_check(box: Box) -> bool:
            return box.state != Box.State.BLOCKED

        def qtree_check(node: QTree) -> bool:
            return node.box.state != Box.State.BLOCKED

        if is_grid(self.data):
            return grid_check

        if is_qtree(self.data):
            return qtree_check

    def __neighbours(self, element: tuple[int, int] | QTree):
        check = self.check_wrapper()

        if is_grid(self.data):
            return self.data.neighbours(element, check)

        if is_qtree(self.data):
            return element.neighbours(check)

    def __bfs(self):
        visited = {self.start: None}
        queue = deque([self.start])

        while queue:
            current = queue.popleft()
            neighbours = self.__neighbours(current)

            for neighbour in neighbours:
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited[neighbour] = current

        path = []
        path_element = self.end

        while path_element in visited:
            path.append(path_element)
            path_element = visited[path_element]

        return path

    def __astar(self):
        print('astar')

    def __jps(self):
        print('jps')
