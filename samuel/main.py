# imports
import pygame as py
from pygame.locals import (K_ESCAPE, KEYDOWN)
from game import Game

from time import sleep


# game code
def main():
    # initalize pygame
    py.init()
    py.display.set_caption("Snake")

    # create clock object
    clock = py.time.Clock()

    # create game object
    game = Game()

    # game loop
    running: bool = True
    while running:

        # check for game close
        for event in py.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == py.QUIT:
                running = False

        # update game
        if not game.game_over:
            game.update_screen(py.key.get_pressed())
        else:
            running = False

        # update display
        py.display.update()

        # ticks per second
        clock.tick(game.TICKS)

    game.draw_end_screen()
    py.display.update()
    sleep(5)

    # close pygame
    py.quit()


if __name__ == "__main__":
    main()
