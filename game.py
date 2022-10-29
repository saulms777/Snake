# imports
import pygame as py
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)
from random import randrange
from constants import Constants


class Game(py.sprite.Sprite, Constants):

    # initialize
    def __init__(self) -> None:

        # initialize from Sprite class
        super().__init__()

        # create screen object
        self.screen = py.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # create head object
        self.head = py.Surface((25, 25))
        self.head.fill(self.HEAD_GREEN)

        # create body segment object
        self.segment = py.Surface((25, 25))
        self.segment.fill(self.BODY_GREEN)

        # create apple object
        self.apple = py.Surface((25, 25))
        self.apple.fill(self.APPLE_RED)

        # create snake
        self.snake: list[list] = [
            [350, 400],
            [325, 400],
            [300, 400],
            [275, 400],
            [250, 400]
        ]

        # set default direction
        self.direction: tuple[int, int] = (25, 0)

        # apple values
        self.apple_coords: list[int, int] = self.generate_apple()

    # generate new apple coords
    def generate_apple(self) -> list[int, int]:

        # generate x value of apple
        apple_x: int = 0
        loop = True
        while loop:
            apple_x = randrange(0, self.SCREEN_WIDTH, 25)
            if apple_x not in [el[0] for el in self.snake]:
                loop = False

        # generate y value of apple
        apple_y: int = 0
        loop = True
        while loop:
            apple_y = randrange(0, self.SCREEN_HEIGHT, 25)
            if apple_y not in [el[1] for el in self.snake]:
                loop = False

        return [apple_x, apple_y]

    # update display
    def update(self, pressed_keys) -> None:

        # set bg to white
        self.screen.fill((255, 255, 255))

        # change direction if key pressed
        key_directions: dict[int, tuple[int, int]] = {
            K_UP: (0, -25),
            K_DOWN: (0, 25),
            K_LEFT: (-25, 0),
            K_RIGHT: (25, 0)
        }
        for key in key_directions:
            if pressed_keys[key]:
                self.direction = key_directions[key]

        # draw snake head
        old_position: list[int, int] = self.snake[0]
        self.snake.insert(0, [old_position[0] + self.direction[0], old_position[1] + self.direction[1]])
        self.screen.blit(self.head, self.snake[0])

        # check if apple was eaten
        if self.snake[0] == self.apple_coords:
            self.apple_coords = self.generate_apple()
        else:
            self.snake.pop()

        # draw body segments
        for segment in self.snake[1:]:
            self.screen.blit(self.segment, segment)

        # draw apple
        self.screen.blit(self.apple, self.apple_coords)

    # check if game over
    def game_over_check(self) -> bool:

        # check if snake crashed into itself
        if len(self.snake) == len(set(map(tuple, self.snake))):

            # check if hit a wall
            head_coords: list[int, int] = self.snake[0]
            if 0 < head_coords[0] < self.SCREEN_WIDTH and 0 < head_coords[1] < self.SCREEN_HEIGHT:
                return False

        return True
