from modules.grid import Grid
from modules.qtree import QTree
from modules.image import Image
from modules.wrapper import Wrapper
from modules.distance import Distance
from modules.pathfinder import Pathfinder


# TODO Diagonal paths
# TODO Better image generation from ndarray (with scikit-image)
# TODO Risk maps by different criteria

def test_pathfinder(image, wrapper, algorithm):
    for distance in Distance.Algorithm:
        wrapper.distance.algorithm = distance

        pathfinder = Pathfinder(wrapper, (4990, 5035), (880, 1510))
        pathfinder.algorithm = algorithm

        path = pathfinder.execute()

        data_name = str.lower(type(wrapper.data).__name__)
        algorithm_name = str.lower(algorithm.name)
        distance_name = str.lower(distance.name)

        save_path = f'data/{data_name}/{data_name}_{algorithm_name}_{distance_name}.png'
        image.save(wrapper, save_path, path)


def main():
    image = Image('data/big_map.png')

    grid = Grid(image.pixels)

    qtree = QTree(0, 0, image.width(), image.height())
    qtree.divide(image.pixels)

    grid_wrapper = Wrapper(grid)
    qtree_wrapper = Wrapper(qtree)

    image.save(grid_wrapper, 'data/grid/grid.png')
    image.save(qtree_wrapper, 'data/qtree/qtree.png')

    test_pathfinder(image, grid_wrapper, Pathfinder.Algorithm.ASTAR)
    test_pathfinder(image, qtree_wrapper, Pathfinder.Algorithm.ASTAR)


if __name__ == '__main__':
    main()
