# imports
import pygame as py
from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)
from random import randrange
from constants import Constants


class Game(Constants):

    # initialize
    def __init__(self) -> None:

        # create screen object
        self.screen = py.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # create background objects
        self.border = py.Surface((self.SIZE, self.SIZE))
        self.border.fill(self.BORDER_GREEN)
        self.light = py.Surface((self.SIZE, self.SIZE))
        self.light.fill(self.LIGHT_GREEN)
        self.dark = py.Surface((self.SIZE, self.SIZE))
        self.dark.fill(self.DARK_GREEN)

        # set snake default position
        middle_x: int = int(self.SCREEN_WIDTH / self.SIZE // 2) * self.SIZE
        middle_y: int = self.TITLE_HEIGHT + int((self.SCREEN_HEIGHT - self.TITLE_HEIGHT) / self.SIZE // 2) * self.SIZE
        self.snake: list[list[int, int]] = [
            [middle_x + 2 * self.SIZE, middle_y],
            [middle_x + self.SIZE, middle_y],
            [middle_x, middle_y],
            [middle_x - self.SIZE, middle_y],
            [middle_x - 2 * self.SIZE, middle_y]
        ]

        # create snake objects
        self.head = py.Surface((self.SIZE, self.SIZE))
        self.head.fill(self.HEAD_BLUE)
        self.segment = py.Surface((self.SIZE, self.SIZE))
        self.segment.fill(self.BODY_BLUE)

        # create apple object
        self.apple_coords: list[int, int] = self.generate_apple()
        self.apple = py.Surface((self.SIZE, self.SIZE))
        self.apple.fill(self.APPLE_RED)

        # set default direction
        self.direction: tuple[int, int] = (self.SIZE, 0)

        # points
        self.points: int = 0

        # game over
        self.game_over: bool = False

    # generate new apple coords
    def generate_apple(self) -> list[int, int]:

        # generate x value of apple
        apple_x: int = 0
        loop = True
        while loop:
            apple_x = randrange(self.SIZE, self.SCREEN_WIDTH - self.SIZE, self.SIZE)
            if apple_x not in [el[0] for el in self.snake]:
                loop = False

        # generate y value of apple
        apple_y: int = 0
        loop = True
        while loop:
            apple_y = randrange(self.TITLE_HEIGHT + self.SIZE, self.SCREEN_HEIGHT - self.SIZE, self.SIZE)
            if apple_y not in [el[1] for el in self.snake]:
                loop = False

        return [apple_x, apple_y]

    # game over check
    def game_over_check(self, head_coords: list[int, int]) -> bool:

        # check if snake crashed into itself
        if head_coords not in self.snake:

            # check if hit a wall
            if self.SIZE <= head_coords[0] <= self.SCREEN_WIDTH - 2 * self.SIZE \
                    and self.TITLE_HEIGHT + self.SIZE <= head_coords[1] <= self.SCREEN_HEIGHT - 2 * self.SIZE:
                return False

        return True

    # update display
    def update(self, pressed_keys) -> None:

        # keys and directions
        key_directions: dict[int, tuple[int, int]] = {
            K_w: (0, -self.SIZE),
            K_s: (0, self.SIZE),
            K_a: (-self.SIZE, 0),
            K_d: (self.SIZE, 0),
            K_UP: (0, -self.SIZE),
            K_DOWN: (0, self.SIZE),
            K_LEFT: (-self.SIZE, 0),
            K_RIGHT: (self.SIZE, 0)
        }

        # change direction if key pressed
        for key, instruction in key_directions.items():
            if pressed_keys[key]:

                # check if input is not opposite direction
                if not (abs(instruction[0]) == abs(self.direction[0])
                        or abs(instruction[1]) == abs(self.direction[1])):
                    self.direction = key_directions[key]

        # check for game end
        new_position: list[int, int] = [self.snake[0][0] + self.direction[0],
                                        self.snake[0][1] + self.direction[1]]
        if self.game_over_check(new_position):
            self.game_over = True
        else:

            # draw background
            self.screen.fill(self.WHITE)

            # draw border
            game_height: int = int((self.SCREEN_HEIGHT - self.TITLE_HEIGHT) / self.SIZE)
            game_width: int = int(self.SCREEN_WIDTH / self.SIZE)
            for column in range(game_height):
                for row in range(game_width):
                    if row in (0, game_width - 1) or column in (0, game_height - 1):
                        self.screen.blit(self.border, (self.SIZE * row, self.TITLE_HEIGHT + self.SIZE * column))

            # draw checkerboard pattern
            for column in range(game_height - 2):
                for row in range(game_width - 2):
                    if (row + column) % 2 == 0:
                        self.screen.blit(self.dark,
                                         (self.SIZE + self.SIZE * row,
                                          self.TITLE_HEIGHT + self.SIZE + self.SIZE * column))
                    else:
                        self.screen.blit(self.light,
                                         (self.SIZE + self.SIZE * row,
                                          self.TITLE_HEIGHT + self.SIZE + self.SIZE * column))

            # draw snake head
            self.snake.insert(0, new_position)
            self.screen.blit(self.head, self.snake[0])

            # check if apple was eaten
            if self.snake[0] == self.apple_coords:
                self.apple_coords = self.generate_apple()
                self.points += 1
            else:
                self.snake.pop()

            # draw body segments
            for segment in self.snake[1:]:
                self.screen.blit(self.segment, segment)

            # draw apple
            self.screen.blit(self.apple, self.apple_coords)
