import numpy as np
from PIL import Image
from modules.grid import Grid
from modules.qtree import QTree
from modules.wrapper import Wrapper
from modules.distance import Distance
from modules.pathfinder import Pathfinder
from modules.utils import save_image


def test_grid_pathfinder(wrapper: Wrapper):
    pathfinder = Pathfinder(wrapper, (608, 31), (62, 526))
    pathfinder.algorithm = Pathfinder.Algorithm.ASTAR
    path = pathfinder.execute()

    save_image(wrapper.data, 'data\\grid_astar_euclidian.bmp', path)


def test_qtree_pathfinder(wrapper: Wrapper):
    pathfinder = Pathfinder(wrapper, (608, 31), (62, 526))
    pathfinder.algorithm = Pathfinder.Algorithm.ASTAR
    path = pathfinder.execute()

    save_image(wrapper.data, 'data\\qtree_astar_euclidian.bmp', path)


def main():
    image = Image.open('data\\map.bmp')
    image_array = np.asarray(image)

    grid = Grid(image_array)
    save_image(grid, 'data\\grid.bmp')

    qtree = QTree(0, 0, image.width, image.height)
    qtree.divide(image_array)
    save_image(qtree, 'data\\qtree.bmp')

    grid_wrapper = Wrapper(grid)
    grid_wrapper.distance.algorithm = Distance.Algorithm.EUCLIDIAN
    test_grid_pathfinder(grid_wrapper)

    qtree_wrapper = Wrapper(qtree)
    qtree_wrapper.distance.algorithm = Distance.Algorithm.EUCLIDIAN
    test_qtree_pathfinder(qtree_wrapper)


if __name__ == '__main__':
    main()
