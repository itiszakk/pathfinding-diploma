class Config:
    class Path:
        ALLOW_DIAGONAL = True
        ENABLE_SMOOTHING = True

    class QTree:
        MIN_SIZE = 100

    class Grid:
        MIN_SIZE = 100

    class Color:
        UNSAFE = (0, 0, 0)
        MIXED = (102, 102, 102)
        SAFE = (255, 255, 255)
        BORDER = (51, 51, 51)
        PATH = (153, 255, 153)
        VISITED = (153, 204, 255)
        TRAJECTORY = (102, 0, 0)
        POINT = (102, 0, 0)

    class Image:
        BORDER = 5
        TRAJECTORY = 10
        POINT = 15
