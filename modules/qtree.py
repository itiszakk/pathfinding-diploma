import numpy as np
from PIL import Image
from enum import IntEnum
from config import Config
from modules.box import Box
from modules.common import Direction


class QTree:

    class Child(IntEnum):
        NW = 0
        NE = 1
        SW = 2
        SE = 3

    class Direction(IntEnum):
        N = 0
        E = 1
        S = 2
        W = 3

    def __init__(self, x, y, w, h):
        self.depth = 0
        self.box = Box(x, y, w, h)
        self.parent: QTree = None
        self.children: list[QTree] = []

    def __repr__(self):
        return (f'QTree('
                f'box={self.box}, '
                f'depth={self.depth}')

    def is_leaf(self):
        return not self.children

    def get(self, x, y):
        if self.is_leaf():
            return self

        for node in self.children:
            if node.box.contains(x, y):
                return node.get(x, y)

    def add_child(self, node: 'QTree'):
        node.depth = self.depth + 1
        node.parent = self
        self.children.append(node)

    def search_children(self):
        if self.is_leaf():
            return [self]

        children = []
        for node in self.children:
            children.extend(node.search_children())

        return children

    def save_image(self, image_path, path=None):
        image = np.empty((self.box.h, self.box.w, 3), dtype=np.uint8)

        children = self.search_children()

        for node in children:
            color = Config.Color.GREEN if path is not None and node in path else node.box.state.color
            image[node.box.y:node.box.y + node.box.h - 1, node.box.x:node.box.x + node.box.w - 1, :] = color
            image[node.box.y:node.box.y + node.box.h, node.box.x + node.box.w - 1, :] = Config.Color.DARKGRAY
            image[node.box.y + node.box.h - 1, node.box.x:node.box.x + node.box.w, :] = Config.Color.DARKGRAY

        image = Image.fromarray(image)
        image.save(image_path)

    def divide(self, image: np.ndarray):
        image_slice = image[self.box.y:self.box.y + self.box.h, self.box.x:self.box.x + self.box.w]

        self.box.state = Box.State.slice_state(image_slice)

        if self.box.state == Box.State.EMPTY or self.box.state == Box.State.BLOCKED:
            return

        w = self.box.w // 2
        h = self.box.h // 2

        if w < Config.QTree.MIN_SIZE or h < Config.QTree.MIN_SIZE:
            return

        nw_child = QTree(self.box.x, self.box.y, w, h)
        self.add_child(nw_child)

        ne_child = QTree(self.box.x + w, self.box.y, w + self.box.w % 2, h)
        self.add_child(ne_child)

        sw_child = QTree(self.box.x, self.box.y + h, w, h + self.box.h % 2)
        self.add_child(sw_child)

        se_child = QTree(self.box.x + w, self.box.y + h, w + self.box.w % 2, h + self.box.h % 2)
        self.add_child(se_child)

        for child in self.children:
            child.divide(image)

    def neighbours(self, check):
        neighbours = []

        for direction in Direction:
            direction_neighbours = self.__get_neighbours_by_direction(direction)

            for neighbour in direction_neighbours:
                if check(neighbour):
                    neighbours.append(neighbour)

        return neighbours

    def __get_neighbours_by_direction(self, direction: Direction):
        neighbour = self.__get_sibling_or_parent_neighbour(direction)
        neighbours = self.__get_neighbours_of_children(neighbour, direction)
        return neighbours

    def __get_sibling_or_parent_neighbour(self, direction: Direction):
        if self.parent is None:
            return None

        siblings = self.parent.children

        if direction == Direction.N:
            if self == siblings[self.Child.SW]:
                return siblings[self.Child.NW]
            if self == siblings[self.Child.SE]:
                return siblings[self.Child.NE]

            node = self.parent.__get_sibling_or_parent_neighbour(direction)

            if node is None or node.is_leaf():
                return node

            if self == siblings[self.Child.NW]:
                return node.children[self.Child.SW]
            else:
                return node.children[self.Child.SE]

        if direction == Direction.E:
            if self == siblings[self.Child.NW]:
                return siblings[self.Child.NE]
            if self == siblings[self.Child.SW]:
                return siblings[self.Child.SE]

            node = self.parent.__get_sibling_or_parent_neighbour(direction)

            if node is None or node.is_leaf():
                return node

            if self == siblings[self.Child.NE]:
                return node.children[self.Child.NW]
            else:
                return node.children[self.Child.SW]

        if direction == Direction.S:
            if self == siblings[self.Child.NW]:
                return siblings[self.Child.SW]
            if self == siblings[self.Child.NE]:
                return siblings[self.Child.SE]

            node = self.parent.__get_sibling_or_parent_neighbour(direction)

            if node is None or node.is_leaf():
                return node

            if self == siblings[self.Child.SW]:
                return node.children[self.Child.NW]
            else:
                return node.children[self.Child.NE]

        if direction == Direction.W:
            if self == siblings[self.Child.NE]:
                return siblings[self.Child.NW]
            if self == siblings[self.Child.SE]:
                return siblings[self.Child.SW]

            node = self.parent.__get_sibling_or_parent_neighbour(direction)

            if node is None or node.is_leaf():
                return node

            if self == siblings[self.Child.NW]:
                return node.children[self.Child.NE]
            else:
                return node.children[self.Child.SE]

    def __get_neighbours_of_children(self, neighbour: 'QTree', direction: Direction):
        candidates = [] if neighbour is None else [neighbour]
        neighbours = []

        if direction == Direction.N:
            while candidates:
                candidate = candidates.pop(0)

                if candidate.is_leaf():
                    neighbours.append(candidate)
                else:
                    candidates.append(candidate.children[self.Child.SW])
                    candidates.append(candidate.children[self.Child.SE])

        if direction == Direction.E:
            while candidates:
                candidate = candidates.pop(0)

                if candidate.is_leaf():
                    neighbours.append(candidate)
                else:
                    candidates.append(candidate.children[self.Child.NW])
                    candidates.append(candidate.children[self.Child.SW])

        if direction == Direction.S:
            while candidates:
                candidate = candidates.pop(0)

                if candidate.is_leaf():
                    neighbours.append(candidate)
                else:
                    candidates.append(candidate.children[self.Child.NW])
                    candidates.append(candidate.children[self.Child.NE])

        if direction == Direction.W:
            while candidates:
                candidate = candidates.pop(0)

                if candidate.is_leaf():
                    neighbours.append(candidate)
                else:
                    candidates.append(candidate.children[self.Child.NE])
                    candidates.append(candidate.children[self.Child.SE])

        return neighbours

    def print_info(self):
        children = self.search_children()

        for node in children:
            print(node)

        print(f'Elements: {len(self.children)}')
