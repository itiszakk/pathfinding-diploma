import numpy as np
from PIL import Image
from modules.qtree import QTree
from modules.grid import Grid


def print_neighbours(x, y):
    node = qtree.get(x, y)

    print(f'Target: {node}')

    n_neighbours = node.neighbours(QTree.Direction.N)
    e_neighbours = node.neighbours(QTree.Direction.E)
    s_neighbours = node.neighbours(QTree.Direction.S)
    w_neighbours = node.neighbours(QTree.Direction.W)

    print()
    print('NORTH:')
    for neighbour in n_neighbours:
        print(neighbour)

    print()
    print('EAST:')
    for neighbour in e_neighbours:
        print(neighbour)

    print()
    print('SOUTH:')
    for neighbour in s_neighbours:
        print(neighbour)

    print()
    print('WEST:')
    for neighbour in w_neighbours:
        print(neighbour)


if __name__ == '__main__':
    image = Image.open('data\\map.bmp').convert('L')
    image_array = np.asarray(image)

    qtree = QTree(0, 0, image.width, image.height)
    qtree.divide(image_array)
    qtree.save_image('data\\qtree.bmp')

    # grid = Grid(image_array)
    # grid.save_image('data\\grid.bmp')
