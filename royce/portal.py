import pygame as py
from random import randrange
from constants import Constants

class Portal(Constants):
	def __init__(self, color):

		if color == 'orange':
			self.color = self.PORTAL_ORANGE

		else:
			self.color = self.PORTAL_BLUE

		self.portal = py.Surface((25, 25))
		self.portal.fill(self.color)

	def generate_portal(self, snake):

		portal_x = 0
		loop = True
		while loop:
			portal_x = randrange(25, self.SCREEN_WIDTH - 50, 25)
			if portal_x not in [el[0] for el in snake]:
				loop = False

		portal_y: int = 0
		loop = True
		while loop:
		    portal_y = randrange(125, self.SCREEN_HEIGHT - 50, 25)
		    if portal_y not in [el[1] for el in snake]:
		        loop = False

		return [portal_x, portal_y]