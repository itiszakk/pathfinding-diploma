from enum import Enum
from modules.box import Box
from modules.grid import Grid
from modules.qtree import QTree
from modules.common import Utils


class Pathfinder:

    class Algorithm(Enum):
        def __init__(self, index, label):
            self.index = index
            self.label = label

        BFS = 0, 'Breadth-First Search'
        ASTAR = 1, 'A*'
        JPS = 2, 'Jump Point Search'

    def __init__(self, data: Grid | QTree | None = None):
        self.data = data
        self.algorithm = Pathfinder.Algorithm.BFS
        self.start_coordinates = None
        self.end_coordinates = None

    def is_grid_data(self):
        return isinstance(self.data, Grid)

    def is_qtree_data(self):
        return isinstance(self.data, QTree)

    def execute(self):
        methods = [self.__bfs, self.__astar, self.__jps]

        time = Utils.time_ms()
        path = methods[self.algorithm.index]()

        self.__print_info(len(path), Utils.time_ms() - time)

        return path

    def __print_info(self, path_length, time):
        print(f'\n'
              f'Algorithm: {self.algorithm.label}\n'
              f'Data type: {type(self.data).__name__}\n'
              f'Path length: {path_length}\n'
              f'Time: {time} ms')

    def check_wrapper(self):

        def grid_check(box: Box) -> bool:
            return box.state != Box.State.BLOCKED

        def qtree_check(node: QTree) -> bool:
            return node.box.state != Box.State.BLOCKED

        if self.is_grid_data():
            return grid_check

        if self.is_qtree_data():
            return qtree_check

    def __neighbours(self, element: tuple[int, int] | QTree):
        check = self.check_wrapper()

        if self.is_grid_data():
            return self.data.neighbours(element, check)

        if self.is_qtree_data():
            return element.neighbours(check)

    def __bfs(self):
        start = self.data.get(*self.start_coordinates)
        end = self.data.get(*self.end_coordinates)

        visited = {start: None}
        queue = [start]

        while queue:
            current = queue.pop(0)
            neighbours = self.__neighbours(current)

            for neighbour in neighbours:
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited[neighbour] = current

        path = []
        path_element = end

        while path_element in visited:
            path.append(path_element)
            path_element = visited[path_element]

        return path

    def __astar(self):
        print('astar')

    def __jps(self):
        print('jps')
