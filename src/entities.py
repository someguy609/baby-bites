
import pygame
import random
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

	def draw(self, surface : pygame.Surface, x_offset, y_offset):
		self.rect.x = self.x * self.tile_size + x_offset
		self.rect.y = self.y * self.tile_size + y_offset
		surface.blit(self.image, self.rect)

	@abstractmethod
	def update(self):
		pass

	@property
	def pos(self):
		return (self.x, self.y)

	@pos.setter
	def pos(self, new_pos : list[int, int]):
		x, y = new_pos
		assert x >= 0 and x < len(self.level[0]) and y >= 0 and y < len(self.level), 'Invalid new position'
		self.x, self.y = new_pos

class Player(Entity):

	def __init__(self, level : list[list[str]], pos : tuple[int, int], tile_size : int):
		super().__init__(level, pos, 'assets/baby/right.png', tile_size)
		self.moved = False
		self.rightImage = self.image
		self.leftImage = pygame.image.load('assets/baby/left.png')
		self.downImage = pygame.image.load('assets/baby/down.png')
  
		self.leftImage = pygame.transform.scale(self.leftImage, (tile_size, tile_size))
		self.downImage = pygame.transform.scale(self.downImage, (tile_size, tile_size))
	
	def update(self):
		if self.moved:
			return
		keys = pygame.key.get_pressed()
		if self.x > 0:
			if keys[pygame.K_LEFT]:
				self.image = self.leftImage
				if self.level[self.y][self.x - 1] != '#':
					self.x -= 1
					self.moved = True
		if self.x < len(self.level[0]) - 1:
			if keys[pygame.K_RIGHT]:
				self.image = self.rightImage
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
				self.image = self.downImage
				if self.level[self.y + 1][self.x] != '#':
					self.y += 1
					self.moved = True

class Enemy(Entity):

	def __init__(self, level : list[list[str]], pos : tuple[int, int], tile_size : int):
		super().__init__(level, pos, 'assets/virus/virus1.png', tile_size)
		self.DIRS = [
			(0, -1),
			(0, 1),
			(-1, 0),
			(1, 0),
		]
		self.frame = [self.image, pygame.image.load('assets/virus/virus2.png')]
		self.frame[1] = pygame.transform.scale(self.frame[1], (tile_size, tile_size))
	
		self.frameCounter = 0
	
	def get_valid_positions(self, pos=None) -> list[tuple[int, int]]:
		if not pos:
			pos = self.pos
		moves = []
		x, y = pos
		for dx, dy in self.DIRS:
			x_, y_ = x + dx, y + dy
			if x_ < 0 or x_ >= len(self.level[0]) or y_ < 0 or y_ >= len(self.level):
				continue
			if self.level[y_][x_] == '#':
				continue
			moves.append((x + dx, y + dy))
		return moves

	def a_star(self, end : tuple[int, int]) -> list:
		self.image = self.frame[self.frameCounter % 2]
  
		self.frameCounter += 1
  
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
			for x_, y_ in self.get_valid_positions(pos):
				h = ((x - x_) ** 2 + (y - y_) ** 2) ** .5
				f_ = g + h
				if f_ < f[y_][x_]:
					f[y_][x_] = f_
					queue.put((f_, (g + 1, path + [(x_, y_)])))
		return []

	def alpha_beta(self, pos, target, depth, alpha=-float('inf'), beta=float('inf'), maximizing=True):
		def heuristic(p1, p2):
			return -((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

		if depth == 0 or self.get_valid_positions(pos) == 0:
			return heuristic(pos, target), pos

		if maximizing:
			max_eval = -float('inf')
			best_move = pos
			for move in self.get_valid_positions(pos):
				eval, _ = self.alpha_beta(move, target, depth - 1, alpha, beta, False)
				if eval > max_eval:
					max_eval = eval
					best_move = move
				alpha = max(alpha, eval)
				if beta <= alpha: 
					break
			return max_eval, best_move
		else:
			min_eval = float('inf')
			best_move = pos
			for move in self.get_valid_positions(pos):
				eval, _ = self.alpha_beta(move, target, depth - 1, alpha, beta, True)
				if eval < min_eval:
					min_eval = eval
					best_move = move
				beta = min(beta, eval)
				if beta <= alpha: 
					break
			return min_eval, best_move

	def update(self, target: tuple[int, int], algo):
		if algo == 'alpha_beta':
			_, best_move = self.alpha_beta(self.pos, target, depth=3)
			assert best_move is not None
			self.pos = best_move
		elif algo == 'a_star':
			best_path = self.a_star(target) 
			assert best_path is not None
			self.x, self.y = best_path[1]

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], tile_size: int, x_offset, y_offset):
        super().__init__()
        self.image = pygame.image.load('assets/wall.png')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] * tile_size + x_offset, pos[1] * tile_size + y_offset)
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

class Food(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], tile_size: int, x_offset: int, y_offset: int):
        super().__init__()
        self.image = pygame.image.load('assets/food.png')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] * tile_size + x_offset, pos[1] * tile_size + y_offset)
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)