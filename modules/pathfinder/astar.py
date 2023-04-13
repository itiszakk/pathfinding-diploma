from pqdict import pqdict

from modules.data.abstract_data import AbstractData
from modules.pathfinder.abstract_pathfinder import AbstractPathfinder


class AStar(AbstractPathfinder):
    def __init__(self, data: AbstractData, start, end):
        super().__init__(data, start, end)

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

        return self.build_path(visited)
