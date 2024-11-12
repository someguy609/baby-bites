import pygame
from abc import ABC, abstractmethod
from queue import PriorityQueue

class Entity(ABC, pygame.sprite.Sprite):

	def __init__(self, level : list[list[str]], pos : tuple[int, int], img : str, tile_size : int):
		super().__init__()
		self.image = pygame.image.load(img)
		self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
		self.rect = self.image.get_rect()
		self.x, self.y = pos
		self.level = level
		self.tile_size = tile_size

	def draw(self, surface : pygame.Surface):
		self.rect.x = self.x * self.tile_size
		self.rect.y = self.y * self.tile_size
		surface.blit(self.image, self.rect)

	@abstractmethod
	def update(self):
		pass

class Player(Entity):

	def __init__(self, level : list[list[str]], pos : tuple[int, int], tile_size : int):
		super().__init__(level, pos, 'assets/baby.png', tile_size)
		self.moved = False
	
	def update(self):
		if self.moved:
			return
		keys = pygame.key.get_pressed()
		if self.x > 0:
			if keys[pygame.K_LEFT]:
				if self.level[self.y][self.x - 1] != '#':
					self.x -= 1
					self.moved = True
		if self.x < len(self.level[0]) - 1:
			if keys[pygame.K_RIGHT]:
				if self.level[self.y][self.x + 1] != '#':
					self.x += 1
					self.moved = True
		if self.y > 0:
			if keys[pygame.K_UP]:
				if self.level[self.y - 1][self.x] != '#':
					self.y -= 1
					self.moved = True
		if self.y < len(self.level) - 1:
			if keys[pygame.K_DOWN]:
				if self.level[self.y + 1][self.x] != '#':
					self.y += 1
					self.moved = True

class Enemy(Entity):

	def __init__(self, level : list[list[str]], pos : tuple[int, int], tile_size : int):
		super().__init__(level, pos, 'assets/virus.png', tile_size)
		self.DIRS = [
			(0, -1),
			(0, 1),
			(-1, 0),
			(1, 0),
		]

	def find_path(self, end : tuple[int, int]) -> list:
		f = [[float('inf') for _ in self.level[0]] for _ in self.level]
		start = (self.x, self.y)
		queue = PriorityQueue()
		queue.put((0, (0, [start])))
		while not queue.empty():
			_, [g, path] = queue.get()
			pos = path[-1]
			if pos == end:
				return path
			x, y = pos
			for dir in self.DIRS:
				dx, dy = dir
				x_, y_ = x + dx, y + dy
				if x_ < 0 or x_ >= len(self.level[0]) or y_ < 0 or y_ >= len(self.level):
					continue
				if self.level[y_][x_] == '#':
					continue
				h = ((x - x_) ** 2 + (y - y_) ** 2) ** .5
				f_ = g + h
				if f_ < f[y_][x_]:
					f[y_][x_] = f_
					queue.put((f_, (g + 1, path + [(x_, y_)])))
		return []

	def minimax(alpha : int, beta : int) -> tuple[int, int]:
		pass

	def update(self, target : tuple[int, int]):
		best_path = self.find_path(target)
		assert best_path is not None
		self.x, self.y = best_path[1]

class Wall(pygame.sprite.Sprite):

	def __init__(self, pos : tuple[int, int], tile_size : int):
		super().__init__()
		self.rect = pygame.rect.Rect(pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size)
	
	def draw(self, surface : pygame.Surface):
		pygame.draw.rect(surface, (255, 0, 0), self.rect)