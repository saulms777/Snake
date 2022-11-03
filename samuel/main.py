# imports
import pygame as py
from pygame.locals import (K_ESCAPE, KEYDOWN)
from game import Game


# game code
def main():
    # initalize pygame
    py.init()
    py.font.init()
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
            if event.type == py.QUIT:
                running = False

        # check if game over
        if not game.game_over:

            # update game
            game.update_screen(py.key.get_pressed())

        else:

            # game over screen
            game.draw_end_screen()
            py.display.update()

            # restart game
            restart: bool = False
            while not restart:
                event = py.event.wait()
                if event.type == py.QUIT:
                    running = False
                    restart = True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    del game
                    game = Game()
                    restart = True

        # update display
        py.display.update()

        # ticks per second
        clock.tick(game.TICKS)

    # close pygame
    py.quit()


if __name__ == "__main__":
    main()
