import pygame as py
from random import randrange
from constants import Constants

class Hole(Constants):

	def __init__(self, size):
		self.size = size
		self.hole = py.Surface((size, size))
		self.hole.fill(self.HOLE_BLACK)

	def generate_hole(self, snake, hole_coords, portal_coords):
		if self.size == 25:

			# generate hole x
			hole_x: int = 0
			loop: bool = True
			while loop:
				hole_x = randrange(25, self.SCREEN_WIDTH - 50, 25)
				if hole_x not in [el[0] for el in snake]:
					if hole_x not in [hole[0][0] for hole in hole_coords]:
						if hole_x not in [portal[0] for portal in portal_coords]:
							loop = False

			# generate hole y
			hole_y: int = 0
			loop: bool = True
			while loop:
				hole_y = randrange(125, self.SCREEN_WIDTH - 50, 25)
				if hole_y not in [el[0] for el in snake]:
					if hole_y not in [hole[0][1] for hole in hole_coords]:
						if hole_y not in [portal[1] for portal in portal_coords]:
							loop = False

			return [[hole_x, hole_y], [None, None]]