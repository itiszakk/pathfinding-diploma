import numpy as np
from PIL import Image
from modules.grid import Grid
from modules.qtree import QTree
from modules.pathfinder import Pathfinder
from modules.utils import save_image


def test_qtree_pathfinder(qtree: QTree):
    pathfinder = Pathfinder(qtree, Pathfinder.Algorithm.BFS, (608, 31), (62, 526))
    path = pathfinder.execute()
    save_image(qtree, 'data\\qtree.bmp')
    save_image(qtree, 'data\\qtree_path.bmp', path)


def test_grid_pathfinder(grid: Grid):
    pathfinder = Pathfinder(grid, Pathfinder.Algorithm.BFS, (608, 31), (62, 526))
    path = pathfinder.execute()
    save_image(grid, 'data\\grid.bmp')
    save_image(grid, 'data\\grid_path.bmp', path)


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
