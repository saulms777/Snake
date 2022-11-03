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

    worker_status = False

    # create game object
    game = Game(worker_status)

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
        over_check, reason, worker_status = game.update(py.key.get_pressed(), worker_status)

        if not over_check:
            over = True
            inputted = False
            greater = False
            anim = 1
            anim_over = True
            # display game over screen
            while over:
                while anim_over:
                    game.game_over_anim(anim, reason)
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
                if reason == 'wall':
                    deathtext = my_font.render('Game Over! You crashed into a wall!', 1, (0,0,0))
                    game.screen.blit(deathtext, (game.SCREEN_WIDTH // 10, game.SCREEN_HEIGHT // 3.5))

                elif reason == 'self':
                    deathtext = my_font.render('Game Over! You crashed into yourself!', 1, (0,0,0))
                    game.screen.blit(deathtext, (game.SCREEN_WIDTH // 11, game.SCREEN_HEIGHT // 3.5))

                elif reason == 'hole':
                    deathtext = my_font.render('Game Over! You fell into a hole!', 1, (0,0,0))
                    game.screen.blit(deathtext, (game.SCREEN_WIDTH // 7, game.SCREEN_HEIGHT // 3.5))

                overtext = my_font.render('You ate {apples} apples!'.format(apples=game.score), 1, (0,0,0))
                rstext = my_font.render('To restart, press R', 1, (0,0,0))
                if greater:
                    hstext = my_font.render('You got a new highscore of {score}!'.format(score=game.score), 1, (0,0,0))
                    game.screen.blit(hstext, (game.SCREEN_WIDTH // 5.5, game.SCREEN_HEIGHT // 2))

                game.screen.blit(overtext, (game.SCREEN_WIDTH // 3, game.SCREEN_HEIGHT // 2.9))
                game.screen.blit(rstext, (game.SCREEN_WIDTH // 3.3, game.SCREEN_HEIGHT//2.5))

                # check for game events
                for event in py.event.get():
                    if event.type == py.QUIT:
                        py.quit()
                        quit()

                    if event.type == py.KEYDOWN:
                        if event.key == py.K_r:
                            over = False
                            del game
                            worker_status = False
                            game = Game(worker_status)

                        if event.key == py.K_ESCAPE:
                            py.quit()
                            quit()

                py.display.update()


        elif reason == 'bomb':
            i = 0
            while i < 16:
                if 0 <= i<= 5:
                    game.screen.fill((255, 255, 0))

                elif 6 <= i <= 10:
                    game.screen.fill((255, 165, 0))

                else:
                    game.screen.fill((255, 0, 0))

                py.display.update()
                i += 1

        elif reason == 'hammer':
            for x in range(2):
                game.screen.fill((0, 255, 128))
                py.display.update()

        elif reason == 'repair':
            for x in range(2):
                game.screen.fill((0, 255, 255))
                py.display.update()


        # update display
        scoretext = my_font.render(str(game.score), 1, (0,0,0))
        game.screen.blit(scoretext, (5, 10))

        py.display.update()
        
        # speed will increase as apples are eaten
        clock.tick(game.speed)

   # close pygame
    py.quit()

if __name__ == "__main__":
    main()