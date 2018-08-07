import pygame
from maze import Maze
from mouse import Mouse
from pygtools import TextBox
from sys import exit
from random import randint


class MazeDisplay:
	"""Controls the pygame portion of a maze."""

	def __init__(self, maze, window):
		"""Set up the game"""
		pygame.key.set_repeat(50)
		window.fill((0, 0, 0))
		self._solving = False
		self._solution = []
		self.window = window
		self.maze = maze
		self.maze.generate_maze()
		self.mouse = Mouse(maze)
		self.mouse_image = pygame.transform.scale(
			pygame.image.load("mouse.png"), (20, 20))
		self.cheese_image = pygame.transform.scale(
			pygame.image.load("cheese.png"), (20, 20))
		self.victory = False;
		self.score_box = MazeDisplay.ScoreBox(pygame.font.Font(None, 30))
		self.make_board()

	def run(self):
		"""Start the main loop."""
		self.running = True
		while self.running:
			self.update()
			self.check_events()

	def update(self):
		"""Update objects on the screen."""
		self.update_mouse()
		self.update_board()
		self.window.blit(pygame.transform.scale(self.score_box.surface,
				(self.score_box.surface.get_width(), 20)), (0, 0))
		self.check_victory()
		#self.window.blit(self.base_board, (0, 0))
		pygame.display.flip()

	def update_board(self):
		"""Blits the board."""
		board = self.base_board.copy()
		if not self.victory:
			board.blit(self.cheese_image,
					(self.maze.goal[0] * 20, self.maze.goal[1] * 20))
		board.blit(
				pygame.transform.rotate(self.mouse_image, 
					90 * self.mouse.facing), 
				(20 * self.mouse.pos[0], 20 * self.mouse.pos[1]))
		self.window.blit(pygame.transform.scale(board, 
				(self.window.get_width(), self.window.get_height() - 20)),
				(0,20))

	def update_mouse(self):
		"""Moves the mouse."""
		if not self._solution:
			if self.mouse.pos == self.maze.start:
				self._solution = self.mouse.breadth_first_solve()[::-1]
			else:
				self._solving = False
		if self._solving:
			if pygame.time.get_ticks() - self._solve_time > 50:
				self.mouse.move(self._solution.pop())
				self._solve_time = pygame.time.get_ticks()

	def check_victory(self):
		"""Checks and handles victory conditions."""
		if self.mouse.pos == self.maze.goal:
			self.victory = True
		if self.victory:
			self.score_box.increment()
			self.maze.generate_maze()
			self.mouse.pos = self.maze.start
			self.make_board()
			self.victory = False

	def make_board(self):
		self.base_board = pygame.Surface(
				(self.maze.size[0] * 20, self.maze.size[1] * 20))
		for col in range(self.maze.size[0]):
			for row in range(self.maze.size[1]):
				if self.maze.get_cell((col, row)):
					cell_color = (150, 150, 150)
				else:
					cell_color = (0, 0, 0)
				pygame.draw.rect(self.base_board, cell_color, 
						pygame.Rect(20 * col, 20 * row, 20, 20))

	def check_events(self):
		"""Check for user input"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				if not self._solving:
					if event.key == pygame.K_UP:
						self.mouse.move(Mouse.NORTH)
					elif event.key == pygame.K_DOWN:
						self.mouse.move(Mouse.SOUTH)
					elif event.key == pygame.K_LEFT:
						self.mouse.move(Mouse.WEST)
					elif event.key == pygame.K_RIGHT:
						self.mouse.move(Mouse.EAST)
					elif event.key == pygame.K_INSERT:
						self.maze.generate_maze()
						self.mouse.pos = self.maze.start
						self.make_board()
						self.score_box.reset()
					if event.key == pygame.K_s:
						self._solution = self.mouse.breadth_first_solve()[::-1]
						self._solve_time = pygame.time.get_ticks()
						self._solving = True
				else:
					if event.key != pygame.K_s:
						self._solution = []

	class ScoreBox(TextBox):

		def __init__(
				self, font, default_text="Score: 0", antialias=True,
				color=(255, 255, 255), background=(0, 0, 0)):
			self.score = 0
			super(MazeDisplay.ScoreBox, self).__init__(
					font, default_text, antialias,
					color, background)

		def increment(self):
			self.score += 1
			self.set_text(self.score)

		def reset(self):
			self.score = 0

		def set_text(self, score):
			super(MazeDisplay.ScoreBox, self).set_text(
					"Score: " + str(self.score))