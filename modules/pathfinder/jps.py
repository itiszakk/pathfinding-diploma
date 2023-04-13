from pqdict import pqdict
from modules.data.grid import Grid
from modules.pathfinder.abstract_pathfinder import AbstractPathfinder


class JPS(AbstractPathfinder):
    def __init__(self, data: Grid, start, end):
        super().__init__(data, start, end)
        assert isinstance(data, Grid)

    def search(self):
        pass
