from Player import Ball
from Player import Player


class Game:

    def __init__(self, id):
        self.id = id
        self.score = [0, 0]
        self.ready = False

        self.p1 = None
        self.p2 = None
        self.ball = Ball(100, 100, 3, 3)

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
        pass

    def touched(self, data):
        # Movement of the ball
        pass

    def draw(self, win):
        if self.p1 is not None and self.p2 is not None:
            self.p1.draw(win)
            self.p2.draw(win)
            self.ball.draw(win)
            print("Drew")

    def update(self):
        if self.p1 is not None and self.p2 is not None:
            self.ball.update()
            self.p1.update()
            self.p2.update()
            print("Game", self, " ", self.p1.x, self.p2.x)
