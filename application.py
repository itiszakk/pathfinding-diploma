from config import Config
from modules import timer
from modules.box import Box
from modules.data.abstract_data import AbstractData
from modules.data.grid import Grid
from modules.data.qtree import QTree
from modules.image import Image
from modules.pathfinder.abstract_pathfinder import AbstractPathfinder
from modules.pathfinder.pathfinder_info import PathfinderInfo
from modules.pathfinder.astar import AStar


# TODO Trajectory smoothing
# TODO Jump Point Search (with grid?)
# TODO Risk maps by different criteria
# TODO Path to special format

def print_pathfinding_info(data: AbstractData,
                           info: PathfinderInfo,
                           distance_method: AbstractData.DistanceMethod,
                           time):

    safe_elements_length = len(data.elements([Box.State.SAFE]))
    path_length = info.path_length()
    visited_length = info.visited_length()
    visited_percent = visited_length / safe_elements_length * 100

    print(f'\n'
          f'Pathfinder: {info.pathfinder_name}\n'
          f'Data: {type(data).__name__}\n'
          f'Distance: {distance_method.name}\n'
          f'Allow diagonal: {Config.Path.ALLOW_DIAGONAL}\n'
          f'Path length: {path_length}\n'
          f'Trajectory length: {info.trajectory_length():.3f}\n'
          f'Visited: {visited_length} ({visited_percent:.3f}% of safe elements)\n'
          f'Time: {time} ms')


def pathfinding(image: Image, pathfinder: AbstractPathfinder, distance_method: AbstractData.DistanceMethod, save_path):
    pathfinder.data.distance_method = distance_method

    start_time = timer.now()
    pathfinder_info: PathfinderInfo = pathfinder.search()
    end_time = timer.now() - start_time

    print_pathfinding_info(pathfinder.data, pathfinder_info, distance_method, end_time)
    image.save(pathfinder.data, save_path, pathfinder_info)


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

    start = 4990, 5035
    end = 880, 1510

    pathfinding(image=image,
                pathfinder=AStar(grid, start, end),
                distance_method=AbstractData.DistanceMethod.EUCLIDIAN,
                save_path='images/grid/grid_astar_euclidian_diagonal.png')

    pathfinding(image=image,
                pathfinder=AStar(qtree, start, end),
                distance_method=AbstractData.DistanceMethod.EUCLIDIAN,
                save_path='images/qtree/qtree_astar_euclidian_diagonal.png')


if __name__ == '__main__':
    main()
