from modules.distance import Distance
from modules.box import Box
from modules.grid import Grid
from modules.qtree import QTree


class Wrapper:
    def __init__(self, data: Grid | QTree):
        self.data = data
        self.distance = Distance()

    def is_grid(self):
        return isinstance(self.data, Grid)

    def is_qtree(self):
        return isinstance(self.data, QTree)

    def neighbours_function(self):
        def grid_neighbours(index: int):
            return self.data.neighbours(index, self.check_function())

        def qtree_neighbours(node: QTree):
            return node.neighbours(self.check_function())

        if isinstance(self.data, Grid):
            return grid_neighbours

        if isinstance(self.data, QTree):
            return qtree_neighbours

    def check_function(self):
        def grid_check_function(box: Box) -> bool:
            return box.state != Box.State.BLOCKED

        def qtree_check_function(node: QTree) -> bool:
            return node.box.state != Box.State.BLOCKED

        if isinstance(self.data, Grid):
            return grid_check_function

        if isinstance(self.data, QTree):
            return qtree_check_function

    def cost_function(self):
        def grid_cost_function(start: int, end: int):
            start_center = self.data.elements[start].center()
            end_center = self.data.elements[end].center()
            return self.distance.get(start_center[0] - end_center[0], start_center[1] - end_center[1])

        def qtree_cost_function(start: QTree, end: QTree):
            start_center = start.box.center()
            end_center = end.box.center()
            return self.distance.get(start_center[0] - end_center[0], start_center[1] - end_center[1])

        if isinstance(self.data, Grid):
            return grid_cost_function

        if isinstance(self.data, QTree):
            return qtree_cost_function

    def heuristic_function(self):
        return self.cost_function()


