from random import randint

class Maze:
	"""The model for a maze.  False cells are walls, true are paths."""

	def __init__(self, (width, height)):
		"""Make a maze and fill it with path cells.

		Keyword arguments:
		width -- the width of the maze in cells, must be greater than 3
		height -- the height of the maze in cells, must be greater than 3
		"""
		if width < 4 or height < 4:
			raise self.MazeTooSmallError((width, height))
		if not width % 2 or not height % 2:
			raise self.MazeEvenError((width, height))
		self.size = (width, height)
		self.goal = (width - 2, height - 2)
		self.start = (1, 1)
		self.cells = [[False for y in range(height)] for x in range(width)]
		self.cells[1][1] = True
		self.cells[width - 2][height - 2] = True

	def change_cell(self, (x, y)):
		"""Changes a cell, if that cell is not the goal or start."""
		if (x, y) not in (self.start, self.goal):
			self.cells[x][y] = not self.cells[x][y]

	def setstart(self, (x, y)):
		"""Changes the maze entrance position"""
		self.start = (x, y)
		if not self.cells[x][y]:
			change_cell((x, y))

	def generate_maze(self):
		"""Randomizes this maze using stupid algorithms"""
		self.cells = [[False for y in range(self.size[1])] 
				for x in range(self.size[0])]
		self.cells[self.start[0]][self.start[1]] = True
		self.cells[self.goal[0]][self.goal[1]] = True
		cell = self.goal
		current_path = []
		unvisited_cells = [(x, y) for y in range(1, self.size[1], 2)
				for x in range(1, self.size[0], 2)]
		unvisited_cells.remove(cell)
		while unvisited_cells:
			neighbors = []
			walls = []
			possible_neighbors = [
					(cell[0] + 2, cell[1]), 
					(cell[0] - 2, cell[1]), 
					(cell[0], cell[1] + 2), 
					(cell[0], cell[1] - 2), 
					]
			possible_walls = [
					(cell[0] + 1, cell[1]), 
					(cell[0] - 1, cell[1]), 
					(cell[0], cell[1] + 1), 
					(cell[0], cell[1] - 1), 
					]
			for i, pos in enumerate(possible_neighbors):
				if self.get_cell(pos) is not None and pos in unvisited_cells:
					neighbors.append(pos)
					walls.append(possible_walls[i])
			if neighbors:
				i = randint(0, len(neighbors) - 1)
				self.change_cell(neighbors[i])
				self.change_cell(walls[i])
				if neighbors[i] in unvisited_cells:
					unvisited_cells.remove(neighbors[i])
				current_path.append(cell)
				cell = neighbors[i]
			else:
				if current_path:
					cell = current_path.pop()

	def setgoal(self, (x, y)):
		"""Changes the maze exit position"""
		self.goal = (x, y)
		if not self.cells[x][y]:
			change_cell((x, y))

	def get_cell(self, (x, y)):
		"""Safely find the value of a cell"""
		if all((x >= 0, y >= 0, x < self.size[0], y < self.size[1])):
			return self.cells[x][y]
		return None

	def __str__(self):
		string = ''
		for y in range(self.size[1]):
			for x in range(self.size[0]):
				if self.cells[x][y]:
					string += "*"
				else:
					string += "#"
			string += '\n'
		return string

	class MazeError(Exception):
		"""Base class for errors involving this maze."""
		pass

	class MazeEvenError(MazeError):
		"""Raised when the maze has an even width or height."""
		def __init__(self, size):
			self.size = size

		def __str__(self):
			return ("The width and height must odd. (" 
					+ str(self.size) + " given)")		

	class MazeTooSmallError(MazeError):
		"""Raised when the maze size is too small."""

		def __init__(self, size):
			self.size = size

		def __str__(self):
			return ("The width and height must be greater than 3. (" 
					+ str(self.size) + " given)")

	class MazeUnsolvableError(MazeError):
		"""Raised when there is no solution to the maze."""

		def __init__(self):
			pass

		def __str__(self):
			return ("The maze has no apparent solution!")