import numpy as np
from PIL import Image
from modules.grid import Grid
from modules.qtree import QTree
from modules.pathfinder import Pathfinder


def test_qtree_pathfinder(qtree: QTree):
    pathfinder = Pathfinder()

    pathfinder.data = qtree
    pathfinder.algorithm = Pathfinder.Algorithm.BFS
    pathfinder.start_coordinates = (608, 31)
    pathfinder.end_coordinates = (62, 526)

    path = pathfinder.execute()

    qtree.save_image('data\\qtree.bmp')
    qtree.save_image('data\\qtree_path.bmp', path)


def test_grid_pathfinder(grid: Grid):
    pathfinder = Pathfinder()

    pathfinder.data = grid
    pathfinder.algorithm = Pathfinder.Algorithm.BFS
    pathfinder.start_coordinates = (608, 31)
    pathfinder.end_coordinates = (62, 526)

    path = pathfinder.execute()

    grid.save_image('data\\grid.bmp')
    grid.save_image('data\\grid_path.bmp', path)


def main():
    image = Image.open('data\\map.bmp')
    image_array = np.asarray(image)

    qtree = QTree(0, 0, image.width, image.height)
    qtree.divide(image_array)
    test_qtree_pathfinder(qtree)

    grid = Grid(image_array)
    test_grid_pathfinder(grid)


if __name__ == '__main__':
    main()
