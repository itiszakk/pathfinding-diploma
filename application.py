from config import Config
from modules import timer
from modules.box import Box
from modules.data.abstract_data import AbstractData
from modules.data.grid import Grid
from modules.data.qtree import QTree
from modules.image import Image
from modules.pathfinder.abstract_pathfinder import AbstractPathfinder
from modules.pathfinder.astar import AStar


# TODO Draw waypoints
# TODO Trajectory smoothing
# TODO Jump Point Search (with grid?)
# TODO Risk maps by different criteria
# TODO Path to special format

def print_pathfinding_info(pathfinder: AbstractPathfinder,
                           distance_method: AbstractData.DistanceMethod,
                           path, visited, time):

    safe_elements = pathfinder.data.elements([Box.State.SAFE])
    path_length = len(path) if path is not None else None

    print(f'\n'
          f'Pathfinder: {type(pathfinder).__name__}\n'
          f'Data: {type(pathfinder.data).__name__}\n'
          f'Distance: {distance_method.name}\n'
          f'Allow diagonal: {Config.Path.ALLOW_DIAGONAL}\n'
          f'Path length: {path_length}\n'
          f'Visited: {len(visited)} ({(len(visited) / len(safe_elements) * 100):.3f}% of safe elements)\n'
          f'Time: {time} ms')


def pathfinding(image: Image, pathfinder: AbstractPathfinder, start, end,
                distance_method: AbstractData.DistanceMethod, save_path: str):
    pathfinder.data.distance_method = distance_method

    start_time = timer.now()
    path, visited = pathfinder.search()
    end_time = timer.now() - start_time

    print_pathfinding_info(pathfinder, distance_method, path, visited, end_time)
    image.save(pathfinder.data, save_path, start, end, path, visited)


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
    image = Image('images/test.png')

    grid = create_grid(image)
    qtree = create_qtree(image)

    start = 4990, 5035
    end = 880, 1510

    pathfinding(image=image,
                pathfinder=AStar(grid, start, end),
                start=start,
                end=end,
                distance_method=AbstractData.DistanceMethod.EUCLIDIAN,
                save_path='images/grid/test.png')

    pathfinding(image=image,
                pathfinder=AStar(qtree, start, end),
                start=start,
                end=end,
                distance_method=AbstractData.DistanceMethod.EUCLIDIAN,
                save_path='images/qtree/test.png')


    # Config.Path.ALLOW_DIAGONAL = True
    # pathfinding(image=image,
    #             pathfinder=AStar(grid, start, end),
    #             distance_method=AbstractData.DistanceMethod.EUCLIDIAN,
    #             save_path='images/grid/grid_astar_euclidian_diagonal.png')
    # pathfinding(image=image,
    #             pathfinder=AStar(grid, start, end),
    #             distance_method=AbstractData.DistanceMethod.MANHATTAN,
    #             save_path='images/grid/grid_astar_manhattan_diagonal.png')
    # pathfinding(image=image,
    #             pathfinder=AStar(qtree, start, end),
    #             distance_method=AbstractData.DistanceMethod.EUCLIDIAN,
    #             save_path='images/qtree/qtree_astar_euclidian_diagonal.png')
    # pathfinding(image=image,
    #             pathfinder=AStar(qtree, start, end),
    #             distance_method=AbstractData.DistanceMethod.MANHATTAN,
    #             save_path='images/qtree/qtree_astar_manhattan_diagonal.png')
    #
    # Config.Path.ALLOW_DIAGONAL = False
    # pathfinding(image=image,
    #             pathfinder=AStar(grid, start, end),
    #             distance_method=AbstractData.DistanceMethod.EUCLIDIAN,
    #             save_path='images/grid/grid_astar_euclidian_cardinal.png')
    # pathfinding(image=image,
    #             pathfinder=AStar(grid, start, end),
    #             distance_method=AbstractData.DistanceMethod.MANHATTAN,
    #             save_path='images/grid/grid_astar_manhattan_cardinal.png')
    # pathfinding(image=image,
    #             pathfinder=AStar(qtree, start, end),
    #             distance_method=AbstractData.DistanceMethod.EUCLIDIAN,
    #             save_path='images/qtree/qtree_astar_euclidian_cardinal.png')
    # pathfinding(image=image,
    #             pathfinder=AStar(qtree, start, end),
    #             distance_method=AbstractData.DistanceMethod.MANHATTAN,
    #             save_path='images/qtree/qtree_astar_manhattan_cardinal.png')


if __name__ == '__main__':
    main()
