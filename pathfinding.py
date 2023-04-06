import numpy as np
from PIL import Image
from modules.qtree import QTreeBuilder


if __name__ == '__main__':
    image = Image.open('data\\map.bmp').convert('L')
    qtree = QTreeBuilder(np.asarray(image))
    qtree.build()
    qtree.save('data\\qtree.bmp')
    print(qtree)
