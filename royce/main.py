# imports
import pygame as py
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    K_r
)
from game import Game
import time


# game code
def main():
    # initalize pygame
    py.init()
    py.font.init()

    py.font.init()
    my_font = py.font.SysFont('Comic Sans MS', 30)

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

        # check if game over
        if not game.update(py.key.get_pressed()):
            over = True
            inputted = False
            greater = False
            anim = 1
            anim_over = True
            # display game over screen
            while over:
                while anim_over:
                    game.game_over_anim(anim)
                    if anim == 20:
                        anim_over = False
                    anim += 1
                    time.sleep(0.1)

                    scoretext = my_font.render(str(game.score), 1, (0,0,0))
                    game.screen.blit(scoretext, (5, 10))

                    py.display.update()

                # add score to list of high scores
                with open('scores.txt', 'a+') as f:
                    f.seek(0)
                    for score in f.readlines():
                        nscore = score.split(' ')[1]
                        nscore = nscore.replace('\n','')
                        if int(game.score) <= int(nscore):
                            inputted = True

                    if not inputted:
                        f.write('%s %s\n' % (str(int(time.time())), str(int(game.score))))
                        inputted = True
                        greater = True

                #display game over info
                game.screen.fill((255,255,255))
                overtext = my_font.render('Game Over! You ate {apples} apples!'.format(apples=game.score), 1, (0,0,0))
                rstext = my_font.render('To restart, press R', 1, (0,0,0))
                if greater:
                    hstext = my_font.render('You got a new highscore of {score}!'.format(score=game.score), 1, (0,0,0))
                    game.screen.blit(hstext, (game.SCREEN_WIDTH // 5.5, game.SCREEN_HEIGHT // 2))

                game.screen.blit(overtext, (game.SCREEN_WIDTH // 6, game.SCREEN_HEIGHT // 3))
                game.screen.blit(rstext, (game.SCREEN_WIDTH // 4, game.SCREEN_HEIGHT//2.5))

                # check for game events
                for event in py.event.get():
                    if event.type == py.QUIT:
                        py.quit()
                        quit()

                    if event.type == py.KEYDOWN:
                        if event.key == py.K_r:
                            over = False
                            del game
                            game = Game()

                        if event.key == py.K_ESCAPE:
                            py.quit()
                            quit()

                py.display.update()

        # update display
        scoretext = my_font.render(str(game.score), 1, (0,0,0))
        game.screen.blit(scoretext, (5, 10))

        py.display.update()
        
        # speed will increase as apples are eaten
        clock.tick(int(game.speed // 1))

   # close pygame
    py.quit()

if __name__ == "__main__":
    main()
