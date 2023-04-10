from modules.data import Data
from modules.distance import Distance
from modules.image import Image
from modules.pathfinder import Pathfinder
from modules.grid import Grid
from modules.qtree import QTree


# TODO Image generation with Data abstract class

# TODO Neighbours by expanded box intersection

# TODO Neighbours only by directions, not all around
# TODO Jump Point Search

# TODO Risk maps by different criteria
# TODO Path to special format

def test_pathfinder(image, data: Data, algorithm):
    for distance in Distance.Algorithm:
        data.distance.algorithm = distance

        pathfinder = Pathfinder(data, (4990, 5035), (880, 1510))
        pathfinder.algorithm = algorithm

        path, visited = pathfinder.execute()

        data_name = str.lower(type(data).__name__)
        algorithm_name = str.lower(algorithm.name)
        distance_name = str.lower(distance.name)

        save_path = f'data/{data_name}/{data_name}_{algorithm_name}_{distance_name}.png'
        image.save(data, save_path, path, visited)


def main():
    image = Image('data/big_map.png')

    grid = Grid(image.pixels)
    qtree = QTree(image.pixels, 0, 0, image.width(), image.height())
    qtree.divide()

    image.save(grid, 'data/grid/grid.png')
    image.save(qtree, 'data/qtree/qtree.png')

    test_pathfinder(image, grid, Pathfinder.Algorithm.ASTAR)
    test_pathfinder(image, qtree, Pathfinder.Algorithm.ASTAR)


if __name__ == '__main__':
    main()
