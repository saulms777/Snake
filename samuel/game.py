# imports
import pygame as py
from random import randrange
from constants import Constants


class Game(Constants):

    # initialize
    def __init__(self) -> None:

        # set screen and background
        self.screen = py.display.set_mode((600, 800))
        self.game_bg = py.image.load("images/game_bg.png").convert()

        # set font
        self.text = py.font.SysFont("calibri", 24, bold=True)

        # set snake default position
        self.snake: list[list[int, int]] = [
            [350, 450],
            [325, 450],
            [300, 450],
            [275, 450],
            [250, 450]
        ]

        # create snake objects
        self.head = py.Surface((25, 25))
        self.head.fill(self.HEAD_BLUE)
        self.segment = py.Surface((25, 25))
        self.segment.fill(self.BODY_BLUE)

        # create apple objects
        self.apple_coords: list[int, int] = self.generate_apple()
        self.apple_dark = py.image.load("images/apple_dark.png").convert()
        self.apple_light = py.image.load("images/apple_light.png").convert()

        # set default direction
        self.direction: tuple[int, int] = (25, 0)

        # points
        self.points: int = 0

        # game over
        self.game_over: bool = False

    # generate new apple coords
    def generate_apple(self) -> list[int, int]:

        # generate apple values
        apple_x: int = 0
        apple_y: int = 0
        loop = True
        while loop:
            apple_x = randrange(25, 575, 25)
            apple_y = randrange(125, 775, 25)
            if [apple_x, apple_y] not in [el for el in self.snake]:
                loop = False

        return [apple_x, apple_y]

    # game over check
    def game_over_check(self, head_coords: list[int, int]) -> bool:

        # check if snake crashed into itself
        if head_coords not in self.snake:

            # check if hit a wall
            if 25 <= head_coords[0] <= 550 \
                    and 125 <= head_coords[1] <= 750:
                return False

        return True

    # update display
    def update_screen(self, pressed_keys) -> None:

        # change direction if key pressed
        for key, instruction in self.KEY_DIRECTIONS.items():
            if pressed_keys[key]:

                # check if input is not opposite direction
                if not (abs(instruction[0]) == abs(self.direction[0])
                        or abs(instruction[1]) == abs(self.direction[1])):
                    self.direction = self.KEY_DIRECTIONS[key]

        # check for game end
        new_position: list[int, int] = [self.snake[0][0] + self.direction[0],
                                        self.snake[0][1] + self.direction[1]]
        if self.game_over_check(new_position):
            self.game_over = True
            return

        # draw background
        self.screen.blit(self.game_bg, (0, 100))

        # check if apple was eaten
        self.snake.insert(0, new_position)
        if new_position == self.apple_coords:
            self.apple_coords = self.generate_apple()
            self.points += 1
        else:
            self.snake.pop()

        # draw snake
        self.screen.blit(self.head, self.snake[0])
        for segment in self.snake[1:]:
            self.screen.blit(self.segment, segment)

        # draw apple
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
        self.screen.blit(self.apple_dark, (275, 400))
        self.screen.blit(self.text.render(f"{self.points}", True, self.BLACK), (305, 403))
        self.screen.blit(self.text.render("Press esc to", True, self.BLACK), (242, 475))
        self.screen.blit(self.text.render("play again", True, self.BLACK), (250, 500))
