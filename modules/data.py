from abc import ABC, abstractmethod
from collections import deque
from enum import Enum, IntEnum

import numpy as np

from config import Config
from modules.distance import Distance


class Box:

    class State(Enum):
        def __init__(self, index, color):
            self.index = index
            self.color = color

        SAFE = 0, Config.Color.SAFE
        MIXED = 1, Config.Color.MIXED
        UNSAFE = 2, Config.Color.UNSAFE

    def __init__(self, x, y, w, h, state=State.SAFE):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.state = state

    def __repr__(self):
        return f'Box(x={self.x}, y={self.y}, w={self.w}, h={self.h}, state={self.state})'

    def contains(self, x, y):
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    def center(self):
        return self.x + self.w // 2, self.y + self.h // 2

    @staticmethod
    def slice_state(data_slice: np.ndarray):
        any_safe = np.any(data_slice == Config.Color.SAFE)
        any_unsafe = np.any(data_slice == Config.Color.UNSAFE)

        if any_safe and not any_unsafe:
            return Box.State.SAFE
        elif not any_safe and any_unsafe:
            return Box.State.UNSAFE

        return Box.State.MIXED


class AbstractData(ABC):

    class Direction(IntEnum):
        N = 0
        E = 1
        S = 2
        W = 3
        NW = 4
        NE = 5
        SE = 6
        SW = 7

        def is_diagonal(self):
            return (self == self.NW or
                    self == self.NE or
                    self == self.SW or
                    self == self.SE)

    class DistanceMethod(IntEnum):
        EUCLIDIAN = 0
        MANHATTAN = 1

    def __init__(self, pixels: np.ndarray):
        self.pixels = pixels
        self.distance_method = AbstractData.DistanceMethod.EUCLIDIAN

    def distance(self, p0, p1):
        match self.distance_method:
            case AbstractData.DistanceMethod.EUCLIDIAN:
                return Distance.euclidian(p0, p1)
            case AbstractData.DistanceMethod.MANHATTAN:
                return Distance.manhattan(p0, p1)

    @staticmethod
    def check(box: Box):
        return box.state == Box.State.SAFE

    @classmethod
    @abstractmethod
    def get(cls, x: int, y: int):
        ...

    @classmethod
    @abstractmethod
    def elements(cls, filters: list[Box.State] | None = None):
        ...

    @classmethod
    @abstractmethod
    def boxes(cls, targets=None):
        ...

    @classmethod
    @abstractmethod
    def neighbour(cls, element, direction: Direction):
        ...

    @classmethod
    @abstractmethod
    def neighbours(cls, element):
        ...

    @classmethod
    @abstractmethod
    def cost(cls, start, end):
        ...

    @classmethod
    @abstractmethod
    def heuristic(cls, start, end):
        ...


class Grid(AbstractData):
    def __init__(self, pixels: np.ndarray):
        super().__init__(pixels)
        self.rows = pixels.shape[0] // Config.Grid.MIN_SIZE
        self.columns = pixels.shape[1] // Config.Grid.MIN_SIZE
        self.boxes_list: list[Box] = []
        self.__init_boxes()

    def get(self, x, y):
        row = y // Config.Grid.MIN_SIZE
        column = x // Config.Grid.MIN_SIZE
        return self.index(row, column)

    def index(self, row, column):
        return row * self.columns + column

    def elements(self, states=None):
        if states is None:
            return self.boxes_list

        elements = []

        for box in self.boxes_list:
            if box.state in states:
                elements.append(box)

        return elements

    def boxes(self, target_list=None):
        if target_list is None:
            return self.boxes_list

        boxes = []

        for target in target_list:
            boxes.append(self.boxes_list[target])

        return boxes

    def direction(self, start: int, end: int):
        x0, y0 = self.boxes_list[start].center()
        x1, y1 = self.boxes_list[end].center()

        if x0 == x1 and y0 < y1:
            return AbstractData.Direction.S
        elif x0 == x1 and y0 > y1:
            return AbstractData.Direction.N
        elif x0 < x1 and y0 == y1:
            return AbstractData.Direction.E
        elif x0 < x1 and y0 < y1:
            return AbstractData.Direction.SE
        elif x0 < x1 and y0 > y1:
            return AbstractData.Direction.NE
        elif x0 > x1 and y0 == y1:
            return AbstractData.Direction.W
        elif x0 > x1 and y0 < y1:
            return AbstractData.Direction.SW
        elif x0 > x1 and y0 > y1:
            return AbstractData.Direction.NW

    def neighbour(self, element: int, direction: AbstractData.Direction):
        row = element // self.columns
        column = element - row * self.columns

        if Config.Path.ALLOW_DIAGONAL and direction.is_diagonal():
            return self.__diagonal_neighbour(row, column, direction)

        return self.__cardinal_neighbour(row, column, direction)

    def neighbours(self, element: int):
        neighbours = []

        for direction in AbstractData.Direction:
            neighbour = self.neighbour(element, direction)

            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def cost(self, start: int, end: int):
        return self.distance(self.boxes_list[start].center(), self.boxes_list[end].center())

    def heuristic(self, start: int, end: int):
        return self.cost(start, end)

    def __cardinal_neighbour(self, row, column, direction: AbstractData.Direction):
        match direction:
            case AbstractData.Direction.N:
                index = self.index(row - 1, column)
                if row > 0 and AbstractData.check(self.boxes_list[index]):
                    return index
            case AbstractData.Direction.E:
                index = self.index(row, column + 1)
                if column < self.columns - 1 and AbstractData.check(self.boxes_list[index]):
                    return index
            case AbstractData.Direction.S:
                index = self.index(row + 1, column)
                if row < self.rows - 1 and AbstractData.check(self.boxes_list[index]):
                    return index
            case AbstractData.Direction.W:
                index = self.index(row, column - 1)
                if column > 0 and AbstractData.check(self.boxes_list[index]):
                    return index

    def __diagonal_neighbour(self, row, column, direction: AbstractData.Direction):
        match direction:
            case AbstractData.Direction.NW:
                index = self.index(row - 1, column - 1)
                if row > 0 and column > 0 and AbstractData.check(self.boxes_list[index]):
                    return index
            case AbstractData.Direction.NE:
                index = self.index(row - 1, column + 1)
                if row > 0 and column < self.columns - 1 and AbstractData.check(self.boxes_list[index]):
                    return index
            case AbstractData.Direction.SE:
                index = self.index(row + 1, column + 1)
                if row < self.rows - 1 and column < self.columns - 1 and AbstractData.check(self.boxes_list[index]):
                    return index
            case AbstractData.Direction.SW:
                index = self.index(row + 1, column - 1)
                if row < self.rows - 1 and column > 0 and AbstractData.check(self.boxes_list[index]):
                    return index

    def __init_boxes(self):
        size = Config.Grid.MIN_SIZE

        assert self.pixels.shape[0] % size == 0 and self.pixels.shape[1] % size == 0, 'Invalid size'

        for row in range(self.rows):
            for column in range(self.columns):
                x = column * size
                y = row * size

                pixels_slice = self.pixels[y:y+size, x:x+size]
                state = Box.slice_state(pixels_slice)

                box = Box(x, y, size, size, state)
                self.boxes_list.append(box)


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
