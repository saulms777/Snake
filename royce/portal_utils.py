# imports
import pygame as py
from random import randrange
from constants import Constants

class Portal(Constants):

	# initialize with a color
	def __init__(self, color) -> None:

		# get a color from Constants
		if color == 'orange':
			self.color: tuple[int, int] = self.PORTAL_ORANGE

		else:
			self.color = self.PORTAL_BLUE

		# create a portal surface with the chosen color
		self.portal = py.Surface((25, 25))
		self.portal.fill(self.color)

	# generate new portal coords
	def generate_portal(self, snake) -> list[int, int]:

		# generate portal x
		portal_x: int = 0
		portal_y: int = 0
		loop: bool = True
		while loop:
			portal_x = randrange(25, self.SCREEN_WIDTH - 50, 25)
			portal_y = randrange(125, self.SCREEN_HEIGHT - 50, 25)
			if [portal_x, portal_y] not in [el for el in snake]:
				loop = False

		return [portal_x, portal_y]