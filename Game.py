from Player import Ball
from Player import Player
import pygame

pygame.font.init()


class Game:

    def __init__(self, id):
        self.id = id
        self.score = [0, 0]
        self.ready = False

        self.sets = list()
        self.p1 = None
        self.p2 = None
        self.recieved = [False, False]
        self.ball = Ball(400, 200, self)

    def connected(self):
        return self.ready

    def display_winner(self, win):
        if len(self.sets) >= 2:
            p1 = 0
            p2 = 0
            for set in self.sets:
                if set == 0:
                    p1 += 1
                else:
                    p2 += 1
            if p1 > p2:
                winner_font = pygame.font.SysFont("comicsans", 100)
                winner_announce = winner_font.render("Ganó Player 1", 1, (255, 0, 0), True)
                win.blit(winner_announce, (300, 200))
            elif p1 < p2:
                winner_font = pygame.font.SysFont("comicsans", 100)
                winner_announce = winner_font.render("Ganó Player 2", 1, (255, 0, 0), True)
                win.blit(winner_announce, (300, 200))
            else:
                return

    def winner(self):
        if len(self.sets) >= 2:
            p1 = 0
            p2 = 0
            for set in self.sets:
                if set == 0:
                    p1 += 1
                else:
                    p2 += 1
            if p1 > p2:
                return True
            elif p1 < p2:
                return True
        return False

    def get_player(self, player, p):
        if p == 0:
            self.p1 = player
        else:
            self.p2 = player

    def set_reset(self):
        self.score[0] = 0
        self.score[1] = 0

    def draw(self, win):
        court = pygame.image.load("images\\court.png")
        font = pygame.font.SysFont("comicsans", 80)
        set_font = pygame.font.SysFont("comicsans", 40)
        score_1 = font.render(str(self.score[0]), 1, (255, 0, 0), True)
        score_2 = font.render(str(self.score[1]), 1, (255, 0, 0), True)
        sets = set_font.render("Sets", 1, (255, 255, 255), True)
        win.blit(court, (0, 0))
        win.blit(score_1, (500 - score_1.get_width(), 20))
        win.blit(score_2, (520, 20))
        win.blit(sets, (0, 0))
        self.draw_sets(win)

        if self.p1 is not None and self.p2 is not None:
            self.p1.draw(win)
            self.p2.draw(win)
            self.ball.draw(win)

        self.display_winner(win)

    def draw_sets(self, win):
        x = 50
        for i in self.sets:
            if i == 0:
                set = pygame.image.load("images\\p1_score.png")
                win.blit(set, (x, 0))
            elif i == 1:
                set = pygame.image.load("images\\p2_score.png")
                win.blit(set, (x, 0))
            x += 50

    def update(self):
        if self.p1 is not None and self.p2 is not None:
            self.ball.update(self)
            self.p1.update()
            self.p2.update()
