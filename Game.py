from Player import Ball
from Player import Player
import pygame

pygame.font.init()


class Game:

    def __init__(self, id):
        self.id = id
        self.score = [0, 0]
        self.ready = False

        self.p1 = None
        self.p2 = None
        self.recieved = [False, False]
        self.ball = Ball(200, 100, 3, 3, self)

    def connected(self):
        return self.ready

    def winner(self):

        winner = -1
        if self.score[0] == 60:
            print("The winner is player 1")
            winner = 0
        elif self.score[1] == 60:
            print("The winner is player 2")
            winner = 1

        return winner

    def get_player(self, player, p):
        if p == 0:
            self.p1 = player
        else:
            self.p2 = player

    def reset(self):
        self.score[0] = 0
        self.score[1] = 0

    def draw(self, win):
        court = pygame.image.load("images\\court.png")
        font = pygame.font.SysFont("comicsans", 80)
        score_1 = font.render(str(self.score[0]), 1, (255, 0, 0), True)
        score_2 = font.render(str(self.score[1]), 1, (255, 0, 0), True)
        win.blit(court, (0, 0))
        win.blit(score_1, (500-score_1.get_width(), 20))
        win.blit(score_2, (520, 20))
        if self.p1 is not None and self.p2 is not None:
            self.p1.draw(win)
            self.p2.draw(win)
            self.ball.draw(win)

    def update(self):
        if self.p1 is not None and self.p2 is not None:
            self.ball.update(self)
            self.p1.update()
            self.p2.update()
