class Config:
    class QTree:
        MIN_SIZE = 5

    class Grid:
        MIN_SIZE = 10

    class Color:
        BLOCKED = (0, 0, 0)
        EMPTY = (255, 255, 255)
        INTERMEDIATE = (153, 153, 153)
        BORDER = (51, 51, 51)
        PATH = (153, 204, 255)
