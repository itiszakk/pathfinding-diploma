from collections import deque
from enum import IntEnum

import numpy as np

from config import Config
from modules.box import Box
from modules.data.abstract_data import AbstractData


class QTree(AbstractData):

    class Child(IntEnum):
        NW = 0
        NE = 1
        SW = 2
        SE = 3

    def __init__(self, pixels: np.ndarray, x, y, w, h):
        super().__init__(pixels)
        self.box = Box(x, y, w, h)
        self.depth = 0
        self.parent: QTree = None
        self.children: list[QTree] = []

    def __repr__(self):
        return f'QTree(box={self.box}, depth={self.depth})'

    def is_leaf(self):
        return not self.children

    def add_child(self, node: 'QTree'):
        node.depth = self.depth + 1
        node.parent = self
        self.children.append(node)

    def get(self, x, y):
        if self.is_leaf():
            return self

        for node in self.children:
            if node.box.contains(x, y):
                return node.get(x, y)

    def elements(self):
        if self.is_leaf():
            return [self]

        children = []
        for node in self.children:
            children.extend(node.elements())

        return children

    def boxes(self, target_list=None):
        boxes = []

        if target_list is None:
            elements = self.elements()

            for element in elements:
                boxes.append(element.box)

            return boxes

        for target in target_list:
            boxes.append(target.box)

        return boxes

    def divide(self):
        x, y, w, h = self.box.x, self.box.y, self.box.w, self.box.h

        pixels_slice = self.pixels[y:y + h, x:x + w]
        self.box.state = Box.slice_state(pixels_slice)

        if self.box.state != Box.State.MIXED:
            return

        half_w = w // 2
        half_h = h // 2

        if half_w < Config.QTree.MIN_SIZE or half_h < Config.QTree.MIN_SIZE:
            return

        nw_child = QTree(self.pixels, x, y, half_w, half_h)
        self.add_child(nw_child)

        ne_child = QTree(self.pixels, x + half_w, y, half_w + w % 2, half_h)
        self.add_child(ne_child)

        sw_child = QTree(self.pixels, x, y + half_h, half_w, half_h + h % 2)
        self.add_child(sw_child)

        se_child = QTree(self.pixels, x + half_w, y + half_h, half_w + w % 2, half_h + h % 2)
        self.add_child(se_child)

        for child in self.children:
            child.divide()

    def neighbour(self, node: 'QTree', direction: AbstractData.Direction):
        if Config.Path.ALLOW_DIAGONAL and direction.is_diagonal():
            diagonal_neighbour = self.__diagonal_neighbour(node, direction)
            return [diagonal_neighbour] if diagonal_neighbour is not None else []

        return self.__cardinal_neighbours(node, direction)

    def neighbours(self, node: 'QTree'):
        neighbours = set()

        for direction in AbstractData.Direction:
            direction_neighbours = self.neighbour(node, direction)

            for neighbour in direction_neighbours:
                neighbours.add(neighbour)

        return neighbours

    def cost(self, start: 'QTree', end: 'QTree'):
        return self.distance(start.box.center(), end.box.center())

    def heuristic(self, start: 'QTree', end: 'QTree'):
        return self.cost(start, end)

    def __cardinal_neighbours(self, node: 'QTree', direction):
        equal_or_greater = self.__get_equal_or_greater_neighbour(node, direction)
        candidates = self.__get_smaller_neighbours(equal_or_greater, direction)

        neighbours = []

        for candidate in candidates:
            if AbstractData.check(candidate.box):
                neighbours.append(candidate)

        return neighbours

    def __diagonal_neighbour(self, node: 'QTree', direction):
        candidate = None

        match direction:
            case AbstractData.Direction.NW:
                candidate = self.get(node.box.x - 1, node.box.y - 1)
            case AbstractData.Direction.NE:
                candidate = self.get(node.box.x + node.box.w, node.box.y - 1)
            case AbstractData.Direction.SE:
                candidate = self.get(node.box.x + node.box.w, node.box.y + node.box.h)
            case AbstractData.Direction.SW:
                candidate = self.get(node.box.x - 1, node.box.y + node.box.h)

        return candidate if candidate is not None and AbstractData.check(candidate.box) else None

    def __get_equal_or_greater_neighbour(self, node: 'QTree', direction: AbstractData.Direction):
        if node.parent is None:
            return None

        match direction:
            case AbstractData.Direction.N:
                if node == node.parent.children[node.Child.SW]:
                    return node.parent.children[node.Child.NW]
                elif node == node.parent.children[node.Child.SE]:
                    return node.parent.children[node.Child.NE]

                next_node = self.__get_equal_or_greater_neighbour(node.parent, direction)

                if next_node is None or next_node.is_leaf():
                    return next_node

                if node == node.parent.children[node.Child.NW]:
                    return next_node.children[node.Child.SW]

                return next_node.children[node.Child.SE]

            case AbstractData.Direction.E:
                if node == node.parent.children[node.Child.NW]:
                    return node.parent.children[node.Child.NE]
                elif node == node.parent.children[node.Child.SW]:
                    return node.parent.children[node.Child.SE]

                next_node = self.__get_equal_or_greater_neighbour(node.parent, direction)

                if next_node is None or next_node.is_leaf():
                    return next_node

                if node == node.parent.children[node.Child.NE]:
                    return next_node.children[node.Child.NW]

                return next_node.children[node.Child.SW]

            case AbstractData.Direction.S:
                if node == node.parent.children[node.Child.NW]:
                    return node.parent.children[node.Child.SW]
                elif node == node.parent.children[node.Child.NE]:
                    return node.parent.children[node.Child.SE]

                next_node = self.__get_equal_or_greater_neighbour(node.parent, direction)

                if next_node is None or next_node.is_leaf():
                    return next_node

                if node == node.parent.children[node.Child.SW]:
                    return next_node.children[node.Child.NW]

                return next_node.children[node.Child.NE]

            case AbstractData.Direction.W:
                if node == node.parent.children[node.Child.NE]:
                    return node.parent.children[node.Child.NW]
                elif node == node.parent.children[node.Child.SE]:
                    return node.parent.children[node.Child.SW]

                next_node = self.__get_equal_or_greater_neighbour(node.parent, direction)

                if next_node is None or next_node.is_leaf():
                    return next_node

                if node == node.parent.children[node.Child.NW]:
                    return next_node.children[node.Child.NE]

                return next_node.children[node.Child.SE]

    def __get_smaller_neighbours(self, node: 'QTree', direction: AbstractData.Direction):
        neighbours = []
        candidates = deque()

        if node is not None:
            candidates.append(node)

        while candidates:
            candidate = candidates.popleft()

            if candidate.is_leaf():
                neighbours.append(candidate)
                continue

            match direction:
                case AbstractData.Direction.N:
                    candidates.append(candidate.children[QTree.Child.SW])
                    candidates.append(candidate.children[QTree.Child.SE])
                case AbstractData.Direction.E:
                    candidates.append(candidate.children[QTree.Child.NW])
                    candidates.append(candidate.children[QTree.Child.SW])
                case AbstractData.Direction.S:
                    candidates.append(candidate.children[QTree.Child.NW])
                    candidates.append(candidate.children[QTree.Child.NE])
                case AbstractData.Direction.W:
                    candidates.append(candidate.children[QTree.Child.NE])
                    candidates.append(candidate.children[QTree.Child.SE])

        return neighbours
