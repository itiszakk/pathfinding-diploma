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

    def elements(self, states=None):
        candidates = self.__search_children()

        if states is None:
            return candidates

        elements = []

        for node in candidates:
            if node.box.state in states:
                elements.append(node)

        return elements

    def boxes(self, targets=None):
        boxes = []

        if targets is None:
            elements = self.elements()

            for element in elements:
                boxes.append(element.box)

            return boxes

        for target in targets:
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

    def direction(self, start: 'QTree', end: 'QTree'):
        return self.Direction.direction(start.box, end.box)

    def neighbour(self, element: 'QTree', direction: AbstractData.Direction):
        if Config.Path.ALLOW_DIAGONAL and direction.is_diagonal():
            diagonal_neighbour = self.__diagonal_neighbour(element, direction)
            return [diagonal_neighbour] if diagonal_neighbour is not None else []

        return self.__cardinal_neighbours(element, direction)

    def neighbours(self, element: 'QTree'):
        neighbours = set()

        for direction in AbstractData.Direction:
            direction_neighbours = self.neighbour(element, direction)

            for neighbour in direction_neighbours:
                neighbours.add(neighbour)

        return neighbours

    def cost(self, start: 'QTree', end: 'QTree'):
        return self.distance(start.box.center(), end.box.center())

    def heuristic(self, start: 'QTree', end: 'QTree'):
        return self.cost(start, end)

    def __search_children(self):
        if self.is_leaf():
            return [self]

        children = []
        for node in self.children:
            children.extend(node.__search_children())

        return children

    def __cardinal_neighbours(self, element: 'QTree', direction: AbstractData.Direction):
        equal_or_greater = self.__get_equal_or_greater_neighbour(element, direction)
        candidates = self.__get_smaller_neighbours(equal_or_greater, direction)

        neighbours = []

        for candidate in candidates:
            if AbstractData.check(candidate.box):
                neighbours.append(candidate)

        return neighbours

    def __diagonal_neighbour(self, element: 'QTree', direction: AbstractData.Direction):
        candidate = None

        match direction:
            case AbstractData.Direction.NW:
                candidate = self.get(element.box.x - 1, element.box.y - 1)
            case AbstractData.Direction.NE:
                candidate = self.get(element.box.x + element.box.w, element.box.y - 1)
            case AbstractData.Direction.SE:
                candidate = self.get(element.box.x + element.box.w, element.box.y + element.box.h)
            case AbstractData.Direction.SW:
                candidate = self.get(element.box.x - 1, element.box.y + element.box.h)

        return candidate if candidate is not None and AbstractData.check(candidate.box) else None

    def __get_equal_or_greater_neighbour(self, element: 'QTree', direction: AbstractData.Direction):
        if element.parent is None:
            return None

        match direction:
            case AbstractData.Direction.N:
                if element == element.parent.children[element.Child.SW]:
                    return element.parent.children[element.Child.NW]
                elif element == element.parent.children[element.Child.SE]:
                    return element.parent.children[element.Child.NE]

                next_element = self.__get_equal_or_greater_neighbour(element.parent, direction)

                if next_element is None or next_element.is_leaf():
                    return next_element

                if element == element.parent.children[element.Child.NW]:
                    return next_element.children[element.Child.SW]

                return next_element.children[element.Child.SE]

            case AbstractData.Direction.E:
                if element == element.parent.children[element.Child.NW]:
                    return element.parent.children[element.Child.NE]
                elif element == element.parent.children[element.Child.SW]:
                    return element.parent.children[element.Child.SE]

                next_element = self.__get_equal_or_greater_neighbour(element.parent, direction)

                if next_element is None or next_element.is_leaf():
                    return next_element

                if element == element.parent.children[element.Child.NE]:
                    return next_element.children[element.Child.NW]

                return next_element.children[element.Child.SW]

            case AbstractData.Direction.S:
                if element == element.parent.children[element.Child.NW]:
                    return element.parent.children[element.Child.SW]
                elif element == element.parent.children[element.Child.NE]:
                    return element.parent.children[element.Child.SE]

                next_element = self.__get_equal_or_greater_neighbour(element.parent, direction)

                if next_element is None or next_element.is_leaf():
                    return next_element

                if element == element.parent.children[element.Child.SW]:
                    return next_element.children[element.Child.NW]

                return next_element.children[element.Child.NE]

            case AbstractData.Direction.W:
                if element == element.parent.children[element.Child.NE]:
                    return element.parent.children[element.Child.NW]
                elif element == element.parent.children[element.Child.SE]:
                    return element.parent.children[element.Child.SW]

                next_element = self.__get_equal_or_greater_neighbour(element.parent, direction)

                if next_element is None or next_element.is_leaf():
                    return next_element

                if element == element.parent.children[element.Child.NW]:
                    return next_element.children[element.Child.NE]

                return next_element.children[element.Child.SE]

    def __get_smaller_neighbours(self, element: 'QTree', direction: AbstractData.Direction):
        neighbours = []
        candidates = deque()

        if element is not None:
            candidates.append(element)

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
