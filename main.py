# imports
import pygame as py
from pygame.locals import (K_ESCAPE, KEYDOWN)
from game import Game


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
        game.update(py.key.get_pressed())

        # check if game over
        if game.game_over_check():
            break

        # update display
        py.display.update()

        # ticks per second
        clock.tick(game.TICKS)

    # close pygame
    py.quit()


if __name__ == "__main__":
    main()
