import pygame as py
from random import randrange
from constants import Constants

class Bomb(Constants):

	def __init__(self):
		self.bomb = py.Surface((25, 25))
		self.bomb.fill(self.BOMB_GRAY)

	def generate_bomb(self, snake) -> list[int, int]:

		# generate portal x
		bomb_x: int = 0
		loop: bool = True
		while loop:
			bomb_x = randrange(25, self.SCREEN_WIDTH - 50, 25)
			if bomb_x not in [el[0] for el in snake]:
				loop = False

		# generate portal y
		bomb_y: int = 0
		loop: bool = True
		while loop:
		    bomb_y = randrange(125, self.SCREEN_HEIGHT - 50, 25)
		    if bomb_y not in [el[1] for el in snake]:
		        loop = False

		return [bomb_x, bomb_y]