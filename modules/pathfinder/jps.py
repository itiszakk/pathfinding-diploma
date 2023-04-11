from modules.data.abstract_data import AbstractData
from modules.pathfinder.abstract_pathfinder import AbstractPathfinder


class JPS(AbstractPathfinder):
    def __init__(self, data: AbstractData, start, end):
        super().__init__(data, start, end)

    def start(self):
        pass
