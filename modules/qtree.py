from collections import deque
from enum import IntEnum

import numpy as np

from config import Config
from modules.box import Box
from modules.data import Data


class QTree(Data):

    class Child(IntEnum):
        NW = 0
        NE = 1
        SW = 2
        SE = 3

    def __init__(self, pixels: np.ndarray, x, y, w, h):
        super().__init__(pixels)
        self.depth = 0
        self.box = Box(x, y, w, h)
        self.parent: QTree = None
        self.children: list[QTree] = []

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

    def boxes(self):
        boxes = []
        elements = self.elements()

        for element in elements:
            boxes.append(element.box)

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

    def neighbour(self, direction: Data.Direction) -> list['QTree']:
        neighbour = self.__get_sibling_or_parent_neighbour(direction)
        neighbours = self.__get_neighbours_of_children(neighbour, direction)
        return neighbours

    def neighbours(self, node: 'QTree'):
        neighbours = []

        for direction in Data.Direction:
            direction_neighbours = node.neighbour(direction)

            for neighbour in direction_neighbours:
                if Data.check(neighbour.box):
                    neighbours.append(neighbour)

        return neighbours

    def cost(self, start: 'QTree', end: 'QTree'):
        return self.distance.get(start.box.center(), end.box.center())

    def heuristic(self, start: 'QTree', end: 'QTree'):
        return self.cost(start, end)

    def __get_sibling_or_parent_neighbour(self, direction: Data.Direction):
        if self.parent is None:
            return None

        match direction:
            case Data.Direction.N:
                if self == self.parent.children[self.Child.SW]:
                    return self.parent.children[self.Child.NW]
                elif self == self.parent.children[self.Child.SE]:
                    return self.parent.children[self.Child.NE]

                node = self.parent.__get_sibling_or_parent_neighbour(direction)

                if node is None or node.is_leaf():
                    return node

                if self == self.parent.children[self.Child.NW]:
                    return node.children[self.Child.SW]

                return node.children[self.Child.SE]

            case Data.Direction.E:
                if self == self.parent.children[self.Child.NW]:
                    return self.parent.children[self.Child.NE]
                elif self == self.parent.children[self.Child.SW]:
                    return self.parent.children[self.Child.SE]

                node = self.parent.__get_sibling_or_parent_neighbour(direction)

                if node is None or node.is_leaf():
                    return node

                if self == self.parent.children[self.Child.NE]:
                    return node.children[self.Child.NW]

                return node.children[self.Child.SW]

            case Data.Direction.S:
                if self == self.parent.children[self.Child.NW]:
                    return self.parent.children[self.Child.SW]
                elif self == self.parent.children[self.Child.NE]:
                    return self.parent.children[self.Child.SE]

                node = self.parent.__get_sibling_or_parent_neighbour(direction)

                if node is None or node.is_leaf():
                    return node

                if self == self.parent.children[self.Child.SW]:
                    return node.children[self.Child.NW]

                return node.children[self.Child.NE]

            case Data.Direction.W:
                if self == self.parent.children[self.Child.NE]:
                    return self.parent.children[self.Child.NW]
                elif self == self.parent.children[self.Child.SE]:
                    return self.parent.children[self.Child.SW]

                node = self.parent.__get_sibling_or_parent_neighbour(direction)

                if node is None or node.is_leaf():
                    return node

                if self == self.parent.children[self.Child.NW]:
                    return node.children[self.Child.NE]

                return node.children[self.Child.SE]

    def __get_neighbours_of_children(self, neighbour: 'QTree', direction: Data.Direction):
        neighbours = []
        candidates = deque()

        if neighbour is not None:
            candidates.append(neighbour)

        while candidates:
            candidate = candidates.popleft()

            if candidate.is_leaf():
                neighbours.append(candidate)
                continue

            match direction:
                case Data.Direction.N:
                    candidates.append(candidate.children[self.Child.SW])
                    candidates.append(candidate.children[self.Child.SE])
                case Data.Direction.E:
                    candidates.append(candidate.children[self.Child.NW])
                    candidates.append(candidate.children[self.Child.SW])
                case Data.Direction.S:
                    candidates.append(candidate.children[self.Child.NW])
                    candidates.append(candidate.children[self.Child.NE])
                case Data.Direction.W:
                    candidates.append(candidate.children[self.Child.NE])
                    candidates.append(candidate.children[self.Child.SE])

        return neighbours
