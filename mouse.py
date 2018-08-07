from maze import Maze
from random import randint
from pygame import time

class Mouse:
    """Solves mazes."""

    DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
    NORTH = 2
    SOUTH = 0
    EAST = 1
    WEST = 3

    def __init__(self, maze):
        self._maze = maze
        self.pos = maze.start
        self.facing = 2

    def _look(self):
        return tuple([sum(each) for each in 
                zip(Mouse.DIRECTIONS[self.facing], self.pos)])

    def _turn(self):
        self.facing = randint(0, 3)

    def breadth_first_solve(self):
        fringe = self.Queue()
        fringe.push((self.pos, []))
        visited = set()
        while not fringe.isEmpty():
            node = fringe.pop()
            visited.add(node[0])
            if node[0] == self._maze.goal:
                return node[1]
            for successor in self.get_successors(node[0]):
                if successor[0] not in visited:
                    fringe.push((successor[0], node[1] + [successor[1]]))
        raise(Maze.MazeUnsolvableError)

    def get_successors(self, (x, y)):
        """Finds the successors of (x, y)"""
        successors = []
        if self._maze.get_cell((x + 1, y)):
            successors.append(((x + 1, y), self.EAST))
        if self._maze.get_cell((x - 1, y)):
            successors.append(((x - 1, y), self.WEST))
        if self._maze.get_cell((x, y + 1)):
            successors.append(((x, y + 1), self.SOUTH))
        if self._maze.get_cell((x, y - 1)):
            successors.append(((x, y - 1), self.NORTH))
        return successors


    def demo_move(self):
        front_cell = self._look()
        if self._maze.get_cell(front_cell) and randint(0, 1):
            self.pos = front_cell
        else:
            self._turn()

    def move(self, facing):
        self.facing = facing
        if self._maze.get_cell(self._look()):
            self.pos = self._look()

    class Queue(object):
        """Fancy queue!"""
        def __init__(self):
            self._list = []
        
        def push(self, item):
            self._list.insert(0, item)
        
        def pop(self):
            return self._list.pop()
        
        def isEmpty(self):
            return not bool(self._list)

        def __str__(self):
            return str(self._list)