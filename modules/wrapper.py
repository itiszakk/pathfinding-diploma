from modules.box import Box
from modules.distance import Distance
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

    def elements(self):
        if self.is_grid():
            return self.data.elements
        elif self.is_qtree():
            return self.data.search_children()

    def neighbours_function(self):
        def grid_neighbours(index: int):
            return self.data.neighbours(index, self.check_function())

        def qtree_neighbours(node: QTree):
            return node.neighbours(self.check_function())

        if self.is_grid():
            return grid_neighbours
        elif self.is_qtree():
            return qtree_neighbours

    def check_function(self):
        def grid_check_function(box: Box) -> bool:
            return box.state == Box.State.SAFE

        def qtree_check_function(node: QTree) -> bool:
            return node.box.state == Box.State.SAFE

        if self.is_grid():
            return grid_check_function
        elif self.is_qtree():
            return qtree_check_function

    def cost_function(self):
        def grid_cost_function(start: int, end: int):
            return self.distance.get(self.data.element(start).center(), self.data.element(end).center())

        def qtree_cost_function(start: QTree, end: QTree):
            return self.distance.get(start.box.center(), end.box.center())

        if self.is_grid():
            return grid_cost_function
        elif self.is_qtree():
            return qtree_cost_function

    def heuristic_function(self):
        return self.cost_function()
