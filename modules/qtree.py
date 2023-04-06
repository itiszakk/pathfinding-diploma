import numpy as np
from PIL import Image
from enum import Enum, IntEnum

MIN_SIZE = 100

BLACK_COLOR = 0
DARKGRAY_COLOR = 64
LIGHTGRAY_COLOR = 128
WHITE_COLOR = 255


class QTree:

    class Child(IntEnum):
        NW = 0
        NE = 1
        SW = 2
        SE = 3

    class State(Enum):
        def __init__(self, index, color):
            self.index = index
            self.color = color

        EMPTY = 0, WHITE_COLOR
        INTERMEDIATE = 1, LIGHTGRAY_COLOR
        BLOCKED = 2, BLACK_COLOR

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = self.State.EMPTY
        self.parent: QTree = None
        self.children: list[QTree] = []

    def __repr__(self):
        return f'Node(x={self.x}, y={self.y}, width={self.width}, height={self.height}, state={self.state})'

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class QTreeBuilder:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.root = QTree(0, 0, image.shape[1], image.shape[0])

    def __repr__(self):
        nodes = QTreeBuilder.__search(self.root)
        return '\n'.join([str(node) for node in nodes]) + f'\nNodes: {len(nodes)}'

    def build(self):
        QTreeBuilder.__divide(self.image, self.root)

    def save(self, path):
        qtree_image = np.empty(self.image.shape, dtype=self.image.dtype)
        children = QTreeBuilder.__search(self.root)

        for node in children:
            inner_slice = qtree_image[node.y:node.y + node.height - 1, node.x:node.x + node.width - 1]
            inner_slice.fill(node.state.color)

            bottom_slice = qtree_image[node.y:node.y + node.height, node.x + node.width - 1]
            bottom_slice.fill(DARKGRAY_COLOR)

            right_slice = qtree_image[node.y + node.height - 1, node.x:node.x + node.width]
            right_slice.fill(DARKGRAY_COLOR)

        qtree_image = Image.fromarray(qtree_image)
        qtree_image.save(path)

    @staticmethod
    def __divide(image: np.ndarray, node: QTree):
        node_slice = image[node.y:node.y + node.height, node.x:node.x + node.width]

        any_white = np.any(node_slice == WHITE_COLOR)
        any_black = np.any(node_slice == BLACK_COLOR)

        if any_white and not any_black:
            node.state = QTree.State.EMPTY
            return

        if not any_white and any_black:
            node.state = QTree.State.BLOCKED
            return

        if any_white and any_black:
            node.state = QTree.State.INTERMEDIATE
            width = node.width // 2
            height = node.height // 2

            if width <= MIN_SIZE or height <= MIN_SIZE:
                return

            node.add_child(QTree(node.x, node.y, width, height))
            node.add_child(QTree(node.x + width, node.y, width + node.width % 2, height))
            node.add_child(QTree(node.x, node.y + height, width, height + node.height % 2))
            node.add_child(QTree(node.x + width, node.y + height, width + node.width % 2, height + node.height % 2))

            for node in node.children:
                QTreeBuilder.__divide(image, node)

    @staticmethod
    def __search(node: QTree):
        if not node.children:
            return [node]

        children = []
        for child in node.children:
            children.extend(QTreeBuilder.__search(child))

        return children
