import time
import numpy as np
from PIL import Image
from config import Config
from modules.grid import Grid
from modules.qtree import QTree


def time_ms():
    return int(round(time.time() * 1000))


def save_image(data: Grid | QTree, image_path, path=None):
    shape = None
    elements = []

    if isinstance(data, Grid):
        shape = (data.image.shape[0], data.image.shape[1], 3)
        elements = data.elements

    if isinstance(data, QTree):
        shape = (data.box.h, data.box.w, 3)
        elements = data.search_children()

    image = np.empty(shape, dtype=np.uint8)

    for index, element in enumerate(elements):
        path_element = None
        box = element

        if isinstance(data, Grid):
            path_element = index

        if isinstance(data, QTree):
            box = element.box
            path_element = element

        x, y, w, h, state = box.x, box.y, box.w, box.h, box.state

        inner_color = Config.Color.PATH if path is not None and path_element in path else state.color
        border_color = Config.Color.BORDER

        image[y:y+h-1, x:x+w-1, :] = inner_color
        image[y:y+h, x+w-1, :] = border_color
        image[y+h-1, x:x+w, :] = border_color

    image = Image.fromarray(image)
    image.save(image_path)
