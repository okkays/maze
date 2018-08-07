import pygame

class Button(object):
	"""A simple button."""

	def __init__(self, (width, height), default_text="button"):
		self.size = (width, height)
		self.surface = pygame.Surface()


class TextBox(object):
	"""A simple textbox."""

	def __init__(
			self, font, default_text="", antialias=True,
			color=(255, 255, 255), background=(0, 0, 0)):
		self._text = default_text
		self.font = font
		self.antialias = antialias
		self.background = background
		self.color = color
		self.update_surface()

	def set_text(self, text):
		"""Update the surface with different text"""
		self._text = text
		self.update_surface()

	def update_surface(self):
		"""Draws text on a surface for easy access"""
		if self._text != "":
			lines = []
			width = 0
			height = 0
			for line in self._text.splitlines():
				line_surface = self.font.render(line, self.antialias, 
					self.color, self.background)
				if line_surface.get_width() > width:
					width = line_surface.get_width()
				if line_surface.get_height() > height:
					height = line_surface.get_height()
				lines.append(self.font.render(line, self.antialias, 
					self.color, self.background))
			self.surface = pygame.Surface((width,height * len(lines)))
			for i, line in enumerate(lines):
				self.surface.blit(line, (0, i * line.get_height()))
		else:
			self.surface = pygame.Surface((1,1))

	def __len__(self):
		return len(str(self))

	def __eq__(self, equaland):
		return str(self) == equaland

	def __contains__(self, term):
		return str(self).contains(term)

	def __str__(self):
		return self._text

	def __add__(self, summand):
		return str(self) + (str(summand))