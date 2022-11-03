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
from portal_utils import Portal
from bomb_utils import Bomb, Hole, Hammer

class Game(Constants):

    # initialize
    def __init__(self, worker_status) -> None:

        # create screen object
        self.screen = py.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # create head object
        self.head = py.Surface((25, 25))
        self.head.fill(self.HEAD_BLUE)

        # create body segment object
        self.segment = py.Surface((25, 25))
        self.segment.fill(self.BODY_BLUE)

        # create construction costume
        self.head_worker = py.Surface((25, 25))
        self.head_worker.fill(self.HEAD_WORKER)

        self.body_worker = py.Surface((25, 25))
        self.body_worker.fill(self.BODY_WORKER)

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

        # hole objects
        self.holes = [None]
        self.hole_coords = [[None, None]]

        # hammer objects
        self.hammer = None
        self.hammer_coords = [None, None]

        # temporarialy initialize bomb coordinates for use in apple generation
        self.bomb_coords = [None, None]

        # apple values
        self.apple_coords: list[int, int] = self.generate_apple()

        # bomb objects and values
        self.bomb = Bomb()
        self.bomb_coords: list[int, int] = self.bomb.generate_bomb(self.snake, self.hole_coords, [self.portal_o_coords, self.portal_b_coords], self.apple_coords, self.hammer_coords)

        # score
        self.score: int = 0

        # snake speed
        self.speed: int = 10

        # is the snake a construction worker
        self.worker = worker_status

    # generate new apple coords
    def generate_apple(self) -> list[int, int]:

        # generate x value of apple
        apple_x: int = 0
        apple_y: int = 0
        loop = True
        while loop:
            apple_x = randrange(25, self.SCREEN_WIDTH - 50, 25)
            apple_y = randrange(125, self.SCREEN_HEIGHT - 50, 25)
            if [apple_x, apple_y] not in [el for el in self.snake]:
                if [apple_x, apple_y] not in [self.portal_o_coords, self.portal_b_coords]:
                    if [apple_x, apple_y] != self.bomb_coords:
                        if [apple_x, apple_y] not in [hole for hole in self.hole_coords]:
                            if [apple_x, apple_y] != self.hammer_coords:
                                loop = False

        return [apple_x, apple_y]

    # update display
    def update(self, pressed_keys, worker_status) -> None:
        self.worker = worker_status
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

        # draw the portals and bombs onto the screen
        self.screen.blit(self.portal_o.portal, self.portal_o_coords)
        self.screen.blit(self.portal_b.portal, self.portal_b_coords)

        try:
            self.screen.blit(self.bomb.bomb, self.bomb_coords)
        except:
            pass

        # move the snake if it is touching a portal
        for i, el in enumerate(self.snake):
            if el == self.portal_o_coords:
                self.snake[i] = self.portal_b_coords
            elif el == self.portal_b_coords:
                self.snake[i] = self.portal_o_coords

        # check if the moved snake will be out of bounds
        new_position: list[int, int] = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]

        if (new_position[0] <= 0) or (new_position[0] >= self.SCREEN_WIDTH - 25) or (new_position[1] <= 75) or (new_position[1] >= self.SCREEN_HEIGHT - 50):
            return False, 'wall', self.worker

        # check if the snake ran over itself
        elif len(self.snake) != len(set(map(tuple, self.snake))):
            return False, 'self', self.worker

        for m, hole in enumerate(self.hole_coords):
            if new_position == hole:
                if not self.worker:
                    return False, 'hole', self.worker

                elif self.worker:
                    del self.holes[m]
                    del self.hole_coords[m]

                    if len(self.holes) != 1:
                        self.hammer = Hammer()
                        self.hammer_coords = self.hammer.generate_hammer(self.snake, self.hole_coords, [self.portal_b_coords, self.portal_b_coords], self.apple_coords, self.bomb_coords)

                    return True, 'hammer', False

        # if a snake hit a bomb, generate x holes and delete the bomb, run bomb animation by returning 'bomb'
        if new_position == self.bomb_coords:

            for x in range(5):
                t_hole = Hole(25)
                t_hole_coords = t_hole.generate_hole(self.snake, self.hole_coords, [self.portal_o_coords, self.portal_b_coords], self.apple_coords)
                self.holes.append(t_hole)
                self.hole_coords.append(t_hole_coords)
            
            self.bomb_coords = self.bomb.generate_bomb(self.snake, self.hole_coords, [self.portal_o_coords, self.portal_b_coords], self.apple_coords, self.hammer_coords)

            if self.hammer == None:
                self.hammer = Hammer()
                self.hammer_coords = self.hammer.generate_hammer(self.snake, self.hole_coords, [self.portal_b_coords, self.portal_b_coords], self.apple_coords, self.bomb_coords)

            return True, 'bomb', self.worker

        elif new_position == self.hammer_coords:
            del self.hammer
            self.hammer_coords = [-500, -500]

            return True, 'hammer', True

        for i, hole in enumerate(self.hole_coords):
            if hole[0] == None:
                pass
            else:
                self.screen.blit(self.holes[i].hole, self.hole_coords[i])



        # draw the snake
        else:
            try:
                self.screen.blit(self.hammer.hammer, self.hammer_coords)
            except:
                pass

            old_position: list[int, int] = self.snake[0]
            self.snake.insert(0, [old_position[0] + self.direction[0], old_position[1] + self.direction[1]])

            if not self.worker:
                self.screen.blit(self.head, self.snake[0])
            elif self.worker:
                self.screen.blit(self.head_worker, self.snake[0])

            # check if apple was eaten
            if self.snake[0] == self.apple_coords:
                self.apple_coords = self.generate_apple()
                self.score += 1
            else:
                self.snake.pop()

            # draw body segments
            for segment in self.snake[1:]:
                if not self.worker:
                    self.screen.blit(self.segment, segment)

                elif self.worker:
                    self.screen.blit(self.body_worker, segment)    

            # draw apple
            self.screen.blit(self.apple, self.apple_coords)

            return True, None, self.worker

    # snake death animation
    def game_over_anim(self, iteration, reason) -> None:
        self.screen.fill((255, 255, 255))

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

        if reason == 'wall' or reason == 'self':
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

        elif reason == 'hole':

            for i, hole in enumerate(self.hole_coords):
                if hole[0] == None:
                    pass
                else:
                    self.screen.blit(self.holes[i].hole, self.hole_coords[i])

            try:
                old_position: list[int, int] = self.snake[0]
                self.snake.insert(0, [old_position[0] + self.direction[0], old_position[1] + self.direction[1]])
                self.snake.pop()
                self.snake.pop(0)

                self.screen.blit(self.segment, self.snake[0])

                for segment in self.snake[1:]:
                    self.screen.blit(self.segment, segment)

            except:
                pass