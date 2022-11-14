# imports
import pygame as py
from pygame.locals import K_RIGHT, K_ESCAPE, KEYDOWN
from game import Game


# game code
def main():

    # initalize pygame
    py.init()
    py.display.set_caption("Snake")

    # initialize game variables
    clock = py.time.Clock()
    game = Game()
    game_start: bool = False
    running: bool = True

    # game loop
    while running:

        for event in py.event.get():

            # check for game close
            if event.type == py.QUIT:
                running = False

            # game start
            if not game_start and event.type == KEYDOWN and event.key == K_RIGHT:
                game_start = True

        # check if game has started
        if game_start:

            # check if game over
            if not game.game_over:

                # update game
                game.change_direction(py.key.get_pressed())
                game.game_over_check()
                if not game.game_over:
                    game.draw_bg()
                    game.update_snake()
                    game.draw_snake()
                    game.draw_apple()

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
                        game_start = False
                        restart = True

        else:

            # draw on-screen objects
            game.draw_bg()
            game.draw_snake()
            game.draw_apple()

        # update display
        py.display.update()

        # ticks per second
        clock.tick(game.TICKS)

    # close pygame
    py.quit()


if __name__ == "__main__":
    main()
