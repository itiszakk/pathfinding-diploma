from modules import timer
from modules.data.abstract_data import AbstractData
from modules.data.grid import Grid
from modules.data.qtree import QTree
from modules.image import Image
from modules.pathfinder.astar import AStar


# TODO Trajectory smoothing
# TODO Jump Point Search
# TODO Risk maps by different criteria
# TODO Path to special format

def print_pathfinding_info(path, visited):
    print(f'Path boxes: {len(path)}\n'
          f'Visited boxes: {len(visited)}')


def test_astar(image, data: AbstractData):
    for distance_algorithm in AbstractData.DistanceAlgorithm:
        data.distance_algorithm = distance_algorithm

        astar = AStar(data, (4990, 5035), (880, 1510))

        start_time = timer.now()
        path, visited = astar.search()
        end_time = timer.now() - start_time

        data_name = str.lower(type(data).__name__)
        distance = str.lower(distance_algorithm.name)

        print(f'\nAStar(images={data_name}, distance={distance}): {end_time} ms')
        print_pathfinding_info(path, visited)

        save_path = f'images/{data_name}/{data_name}_astar_{distance}.png'
        image.save(data, save_path, path, visited)


def create_grid(image):
    start_time = timer.now()
    grid = Grid(image.pixels)
    end_time = timer.now() - start_time

    print(f'Grid creation: {end_time} ms')
    image.save(grid, 'images/grid/grid.png')

    return grid


def create_qtree(image):
    start_time = timer.now()
    qtree = QTree(image.pixels, 0, 0, image.width(), image.height())
    qtree.divide()
    end_time = timer.now() - start_time

    print(f'QTree creation: {end_time} ms')
    image.save(qtree, 'images/qtree/qtree.png')

    return qtree


def main():
    image = Image('images/big_map.png')

    grid = create_grid(image)
    qtree = create_qtree(image)

    test_astar(image, grid)
    test_astar(image, qtree)


if __name__ == '__main__':
    main()
