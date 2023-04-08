import numpy as np
from enum import IntEnum
from config import Config
from modules.box import Box, Direction
from collections import deque


class QTree:

    class Child(IntEnum):
        NW = 0
        NE = 1
        SW = 2
        SE = 3

    def __init__(self, x, y, w, h):
        self.depth = 0
        self.box = Box(x, y, w, h)
        self.parent: QTree = None
        self.children: list[QTree] = []

    def __repr__(self):
        return (f'QTree('
                f'box={self.box}, '
                f'depth={self.depth})')

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

    def divide(self, image: np.ndarray):
        x, y, w, h = self.box.x, self.box.y, self.box.w, self.box.h

        image_slice = image[y:y+h, x:x+w]
        self.box.state = Box.slice_state(image_slice)

        if self.box.state == Box.State.EMPTY or self.box.state == Box.State.BLOCKED:
            return

        half_w = w // 2
        half_h = h // 2

        if half_w < Config.QTree.MIN_SIZE or half_h < Config.QTree.MIN_SIZE:
            return

        nw_child = QTree(x, y, half_w, half_h)
        self.add_child(nw_child)

        ne_child = QTree(x + half_w, y, half_w + w % 2, half_h)
        self.add_child(ne_child)

        sw_child = QTree(x, y + half_h, half_w, half_h + h % 2)
        self.add_child(sw_child)

        se_child = QTree(x + half_w, y + half_h, half_w + w % 2, half_h + h % 2)
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

        if direction == Direction.N:
            if self == self.parent.children[self.Child.SW]:
                return self.parent.children[self.Child.NW]

            if self == self.parent.children[self.Child.SE]:
                return self.parent.children[self.Child.NE]

            node = self.parent.__get_sibling_or_parent_neighbour(direction)

            if node is None or node.is_leaf():
                return node

            if self == self.parent.children[self.Child.NW]:
                return node.children[self.Child.SW]

            return node.children[self.Child.SE]

        if direction == Direction.E:
            if self == self.parent.children[self.Child.NW]:
                return self.parent.children[self.Child.NE]

            if self == self.parent.children[self.Child.SW]:
                return self.parent.children[self.Child.SE]

            node = self.parent.__get_sibling_or_parent_neighbour(direction)

            if node is None or node.is_leaf():
                return node

            if self == self.parent.children[self.Child.NE]:
                return node.children[self.Child.NW]

            return node.children[self.Child.SW]

        if direction == Direction.S:
            if self == self.parent.children[self.Child.NW]:
                return self.parent.children[self.Child.SW]

            if self == self.parent.children[self.Child.NE]:
                return self.parent.children[self.Child.SE]

            node = self.parent.__get_sibling_or_parent_neighbour(direction)

            if node is None or node.is_leaf():
                return node

            if self == self.parent.children[self.Child.SW]:
                return node.children[self.Child.NW]

            return node.children[self.Child.NE]

        if direction == Direction.W:
            if self == self.parent.children[self.Child.NE]:
                return self.parent.children[self.Child.NW]

            if self == self.parent.children[self.Child.SE]:
                return self.parent.children[self.Child.SW]

            node = self.parent.__get_sibling_or_parent_neighbour(direction)

            if node is None or node.is_leaf():
                return node

            if self == self.parent.children[self.Child.NW]:
                return node.children[self.Child.NE]

            return node.children[self.Child.SE]

    def __get_neighbours_of_children(self, neighbour: 'QTree', direction: Direction):
        neighbours = []
        candidates = deque()

        if neighbour is not None:
            candidates.append(neighbour)

        while candidates:
            candidate = candidates.popleft()

            if candidate.is_leaf():
                neighbours.append(candidate)
                continue

            if direction == Direction.N:
                candidates.append(candidate.children[self.Child.SW])
                candidates.append(candidate.children[self.Child.SE])

            if direction == Direction.E:
                candidates.append(candidate.children[self.Child.NW])
                candidates.append(candidate.children[self.Child.SW])

            if direction == Direction.S:
                candidates.append(candidate.children[self.Child.NW])
                candidates.append(candidate.children[self.Child.NE])

            if direction == Direction.W:
                candidates.append(candidate.children[self.Child.NE])
                candidates.append(candidate.children[self.Child.SE])

        return neighbours

    def print_info(self):
        children = self.search_children()

        for node in children:
            print(node)

        print(f'Elements: {len(self.children)}')
