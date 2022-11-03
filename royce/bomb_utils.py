import pygame as py
from random import randrange
import time
from constants import Constants

class Bomb(Constants):

	def __init__(self):
		self.bomb = py.Surface((25, 25))
		self.bomb.fill(self.BOMB_GRAY)

	def generate_bomb(self, snake, hole_coords, portal_coords, apple_coords, hammer) -> list[int, int]:

		# generate portal x
		bomb_x: int = 0
		bomb_y: int = 0
		loop: bool = True
		while loop:
			bomb_x = randrange(25, self.SCREEN_WIDTH - 50, 25)
			bomb_y = randrange(125, self.SCREEN_HEIGHT - 50, 25)
			if [bomb_x, bomb_y] not in [el for el in snake]:
				if [bomb_x, bomb_y] not in [hole for hole in hole_coords]:
					if [bomb_x, bomb_y] not in [portal for portal in portal_coords]:
						if [bomb_x, bomb_y] != apple_coords:
							if [bomb_x, bomb_y] != hammer:
								loop = False

		return [bomb_x, bomb_y]


class Hole(Constants):

	def __init__(self, size):
		self.size = size
		self.hole = py.Surface((size, size))
		self.hole.fill(self.HOLE_BLACK)

	def generate_hole(self, snake, hole_coords, portal_coords, apple_coords):
		if self.size == 25:

			# generate hole x
			hole_x: int = 0
			hole_y: int = 0
			loop: bool = True
			while loop:
				hole_x = randrange(25, self.SCREEN_WIDTH - 50, 25)
				hole_y = randrange(125, self.SCREEN_WIDTH - 50, 25)
				if [hole_x, hole_y] not in [el for el in snake]:
					if [hole_x, hole_y] not in [portal for portal in portal_coords]:
						if [hole_x, hole_y] not in [hole for hole in hole_coords]:
							if [hole_x, hole_y] != apple_coords:
								loop = False

			return [hole_x, hole_y]

class Hammer(Constants):

	def __init__(self):
		self.hammer = py.Surface((25, 25))
		self.hammer.fill(self.HAMMER_BROWN)

	def generate_hammer(self, snake, hole_coords, portal_coords, apple_coords, bomb_coords):

		hammer_x: int = 0
		hammer_y: int = 0
		loop: bool = True
		while loop:
			hammer_x = randrange(25, self.SCREEN_WIDTH - 50, 25)
			hammer_y = randrange(125, self.SCREEN_WIDTH - 50, 25)
			if [hammer_x, hammer_y] not in [el for el in snake]:
				if [hammer_x, hammer_y] not in [portal for portal in portal_coords]:
					if [hammer_x, hammer_y] not in [hole for hole in hole_coords]:
						if [hammer_x, hammer_y] != apple_coords:
							if [hammer_x, hammer_y] != bomb_coords:
								loop = False

		return [hammer_x, hammer_y]