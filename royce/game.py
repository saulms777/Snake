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
from portal import Portal

class Game(Constants):

    # initialize
    def __init__(self) -> None:

        # create screen object
        self.screen = py.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # create head object
        self.head = py.Surface((25, 25))
        self.head.fill(self.HEAD_BLUE)

        # create body segment object
        self.segment = py.Surface((25, 25))
        self.segment.fill(self.BODY_BLUE)

        # create apple object
        self.apple = py.Surface((25, 25))
        self.apple.fill(self.APPLE_RED)

        # background surfaces
        self.border = py.Surface((25, 25))
        self.border.fill(self.BORDER_GREEN)

        # checkered surfaces
        self.dark = py.Surface((25, 25))
        self.dark.fill(self.DARK_GREEN)

        self.light = py.Surface((25, 25))
        self.light.fill(self.LIGHT_GREEN)

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

        # portal objects and values
        self.portal_o = Portal('orange')
        self.portal_o_coords: list[int, int] = self.portal_o.generate_portal(self.snake)

        self.portal_b = Portal('blue')
        self.portal_b_coords: list[int, int] = self.portal_b.generate_portal(self.snake)

        # apple values
        self.apple_coords: list[int, int] = self.generate_apple()

        # score
        self.score: int = 0

        # snake speed
        self.speed: int = 10

    # generate new apple coords
    def generate_apple(self) -> list[int, int]:

        # generate x value of apple
        apple_x: int = 0
        loop = True
        while loop:
            apple_x = randrange(25, self.SCREEN_WIDTH - 50, 25)
            if apple_x not in [el[0] for el in self.snake] and apple_x != self.portal_o_coords[0] and apple_x != self.portal_b_coords[0]:
                loop = False

        # generate y value of apple
        apple_y: int = 0
        loop = True
        while loop:
            apple_y = randrange(125, self.SCREEN_HEIGHT - 50, 25)
            if apple_y not in [el[1] for el in self.snake] and apple_x != self.portal_o_coords[1] and apple_x != self.portal_b_coords[1]:
                loop = False

        return [apple_x, apple_y]

    # update display
    def update(self, pressed_keys) -> None:
            # change direction if key pressed
            key_directions: dict[int, tuple[int, int]] = {
                K_UP: (0, -25),
                K_DOWN: (0, 25),
                K_LEFT: (-25, 0),
                K_RIGHT: (25, 0)
            }

            # update directions based on key press
            for key in key_directions:
                if pressed_keys[key]:
                    # do not change direction if the new direction is opposite to the old one
                    if ((0 - int(key_directions[key][0])) == self.direction[0]) or ((0 - int(key_directions[key][1])) == self.direction[1]):
                        pass

                    else:
                        self.direction = key_directions[key]

            # draw background
            self.screen.fill((255,255,255))

            # draw border
            game_height: int = int(self.SCREEN_HEIGHT - 100) // 25
            game_width: int = int(self.SCREEN_WIDTH) // 25

            for column in range(game_height):
                for row in range(game_width):
                    if row in (0, game_width - 1) or column in (0, game_height - 1):
                        self.screen.blit(self.border, (25 * row, 75 + 25 * column))

            # draw checkerboard
            for column in range(game_height - 2):
                for row in range(game_width - 2):
                    if (row + column) % 2 == 0:
                        self.screen.blit(self.dark, (25 + 25 * row, 100 + 25 * column))

                    else:
                        self.screen.blit(self.light, (25 + 25 * row, 100 + 25 * column))

            # draw the portals onto the screen
            self.screen.blit(self.portal_o.portal, self.portal_o_coords)
            self.screen.blit(self.portal_b.portal, self.portal_b_coords)

            # move the snake if it is touching a portal
            for i, el in enumerate(self.snake):
                if el == self.portal_o_coords:
                    self.snake[i] = self.portal_b_coords
                elif el == self.portal_b_coords:
                    self.snake[i] = self.portal_o_coords

            # check if the moved snake will be out of bounds
            new_position = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]

            if (new_position[0] <= 0) or (new_position[0] >= self.SCREEN_WIDTH - 25) or (new_position[1] <= 75) or (new_position[1] >= self.SCREEN_HEIGHT - 50):
                return False

            elif len(self.snake) != len(set(map(tuple, self.snake))):
                return False

            # draw the snake
            else:
                old_position: list[int, int] = self.snake[0]
                self.snake.insert(0, [old_position[0] + self.direction[0], old_position[1] + self.direction[1]])
                self.screen.blit(self.head, self.snake[0])

                # check if apple was eaten
                if self.snake[0] == self.apple_coords:
                    self.apple_coords = self.generate_apple()
                    self.score += 1
                    self.speed += 0.5
                else:
                    self.snake.pop()

                # draw body segments
                for segment in self.snake[1:]:
                    self.screen.blit(self.segment, segment)

                # draw apple
                self.screen.blit(self.apple, self.apple_coords)

                return True

    # snake death animation
    def game_over_anim(self, iteration) -> None:
        self.screen.fill((255, 255, 255))

        # draw border
        game_height: int = int(self.SCREEN_HEIGHT - 100) // 25
        game_width: int = int(self.SCREEN_WIDTH) // 25

        # make the surfaces for the color change from blue to red
        self.death_head = py.Surface((25,25))
        self.death_body = py.Surface((25,25))

        # if the snake has finished changing colors, set the fill of those surfaces to black
        try:
            self.death_head.fill(self.DEATH_COLORS_HEAD[iteration - 1])
            self.death_body.fill(self.DEATH_COLORS_BODY[iteration - 1])
        except IndexError:
            self.death_head.fill((0, 0, 0))
            self.death_body.fill((0, 0, 0))

        # make the surface for the exploded snake
        self.death = py.Surface((25,25))
        self.death.fill(self.DEATH_RED)

        for column in range(game_height):
            for row in range(game_width):
                if row in (0, game_width - 1) or column in (0, game_height - 1):
                    self.screen.blit(self.border, (25 * row, 75 + 25 * column))

        # draw checkerboard
        for column in range(game_height - 2):
            for row in range(game_width - 2):
                if (row + column) % 2 == 0:
                    self.screen.blit(self.dark, (25 + 25 * row, 100 + 25 * column))

                else:
                    self.screen.blit(self.light, (25 + 25 * row, 100 + 25 * column))
                
        # for the first 8 frames, the snake only changes color
        if 1 <= iteration <= 8:
            pass

        # explode the snake once, then move all pieces down for the duration of the animation
        else:
            for i, segment in enumerate(self.snake):
                if iteration == 9:
                    seg_coords: list[int, int] = [segment[0], segment[1]]
                    nsegment: list[int, int, bool] = [segment[0] + randrange(-100, 100, 25), segment[1] + randrange(-100, 100, 25), True]
                    while not (25 <= nsegment[0] <= self.SCREEN_WIDTH - 50 and 125 <= nsegment[1] <= self.SCREEN_HEIGHT - 75):
                        nsegment: list[int, int, bool] = [segment[0] + randrange(-100, 100, 25), segment[1] + randrange(-100, 100, 25), True]

                else:
                    seg_coords: list[int, int] = [segment[0], segment[1]]
                    if seg_coords[1] >= self.SCREEN_HEIGHT - 75:
                        nsegment = [segment[0], segment[1], True]
                    else:
                        nsegment: list[int, int, bool] = [segment[0], segment[1] + 25, True]

                self.snake[i] = nsegment


        # color the snake depending on what phase of the animation it's in
        for n, segment in enumerate(self.snake):
            if 1 <= iteration <= 8:
                if n == 0:
                    self.screen.blit(self.death_head, self.snake[n][0:2])

                else:
                    self.screen.blit(self.death_body, self.snake[n][0:2])

            else:
                self.screen.blit(self.death, self.snake[n][0:2])
