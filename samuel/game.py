# imports
import pygame as py
from random import randrange
from constants import Constants
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT


class Game(Constants):

    # initialize
    def __init__(self) -> None:

        # set screen and background
        self.screen = py.display.set_mode((600, 800))
        self.game_bg = py.image.load("images/game_bg.png").convert()

        # set font
        self.text = py.font.SysFont("calibri", 24, bold=True)

        # set snake default position
        self.snake: list[list[int, int]] = [[350, 450],
                                            [325, 450],
                                            [300, 450],
                                            [275, 450],
                                            [250, 450]]

        # create snake objects
        self.head = py.Surface((25, 25))
        self.head.fill(self.HEAD_BLUE)
        self.segment = py.Surface((25, 25))
        self.segment.fill(self.BODY_BLUE)

        # create apple objects
        self.apple_coords: list[int, int] = self.generate_apple()
        self.apple_dark = py.image.load("images/apple_dark.png").convert()
        self.apple_light = py.image.load("images/apple_light.png").convert()

        # other variables
        self.direction: tuple[int, int] = (25, 0)
        self.new_position: list[int, int] = []
        self.points: int = 0
        self.game_over: bool = False

    # change direction
    def change_direction(self, pressed_keys) -> None:

        # directions for each key
        KEY_DIRECTIONS: dict[int, tuple[int, int]] = {K_UP: (0, -25),
                                                      K_DOWN: (0, 25),
                                                      K_LEFT: (-25, 0),
                                                      K_RIGHT: (25, 0)}

        # check if key pressed
        for key, instruction in KEY_DIRECTIONS.items():
            if pressed_keys[key]:

                # prevents snake from self-destructing
                direction = KEY_DIRECTIONS[key]
                if self.snake[1] != [self.snake[0][0] + direction[0], self.snake[0][1] + direction[1]]:
                    self.direction = direction

    # game over check
    def game_over_check(self) -> None:

        # calculate next position
        self.new_position = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]

        # check if snake crashed into itself
        if self.new_position not in self.snake:

            # check if hit a wall
            if 25 <= self.new_position[0] <= 550 and 125 <= self.new_position[1] <= 750:
                return

        self.game_over = True

    # generate new apple coords
    def generate_apple(self) -> list[int, int]:

        # generate apple coords
        apple_x: int = 0
        apple_y: int = 0
        loop = True
        while loop:
            apple_x = randrange(25, 575, 25)
            apple_y = randrange(125, 775, 25)
            if [apple_x, apple_y] not in [el for el in self.snake]:
                loop = False

        return [apple_x, apple_y]

    # draw background
    def draw_bg(self) -> None:

        self.screen.blit(self.game_bg, (0, 100))

    # update snake list
    def update_snake(self) -> None:

        self.snake.insert(0, self.new_position)
        if self.new_position == self.apple_coords:
            self.apple_coords = self.generate_apple()
            self.points += 1
        else:
            self.snake.pop()

    # draw snake
    def draw_snake(self) -> None:

        self.screen.blit(self.head, self.snake[0])
        for segment in self.snake[1:]:
            self.screen.blit(self.segment, segment)

    # draw apple
    def draw_apple(self) -> None:

        if sum(self.apple_coords) % 50 == 0:
            self.screen.blit(self.apple_dark, self.apple_coords)
        else:
            self.screen.blit(self.apple_light, self.apple_coords)

    # end screen
    def draw_end_screen(self) -> None:

        # darken screen
        end_screen = py.image.load("images/ending_bg.png").convert()
        self.screen.blit(end_screen, (0, 100))

        # end screen
        self.screen.blit(self.apple_dark, (276, 400))
        self.screen.blit(self.text.render(f"{self.points}", True, self.BLACK), (306, 403))
        self.screen.blit(self.text.render("Press esc to", True, self.BLACK), (242, 475))
        self.screen.blit(self.text.render("play again", True, self.BLACK), (250, 500))
