import pygame
import time


def intersects(first, other):
    return first.x < other.x + other.width and first.x + first.width > other.x and first.y < other.y + other.height and first.y + first.height > other.y


class Player:

    def __init__(self, x, y, color, id):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = color
        self.id = id
        self.rect = (x, y, self.width, self.height)
        self.vel = 5
        self.swing = (x, y, 0, 0)
        self.racket = Racket(self, 7, 40, 0, -40)

        # Strike booleans
        self.strikeU = False
        self.strikeD = False

        self.timer = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        #if self.is_striking():
        self.racket.draw(win)

    def move(self):
        # We get all the keys that are pressed in the moment
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            if self.id == 1:
                if self.x <= 500:
                    self.x = 501
            else:
                if self.x <= 0:
                    self.x = 1
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            if self.id == 1:
                if self.x + self.width >= 1000:
                    self.x = 1000-self.width-1
            else:
                if self.x + self.width >= 500:
                    self.x = 500-self.width-1
        if keys[pygame.K_UP]:
            self.y -= self.vel
            if self.y <= 0:
                self.y = 1
        if keys[pygame.K_DOWN]:
            self.y += self.vel
            if self.y + self.height >= 500:
                self.y = 500-self.height-1
        if keys[pygame.K_q]:
            self.strikeU = True
        else:
            self.strikeU = False
        if keys[pygame.K_a]:
            self.strikeD = True
        else:
            self.strikeD = False
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
        if self.strikeU:
            self.racket.update(self, -40)
        elif self.strikeD:
            self.racket.update(self, self.height)
        else:
            self.racket.disappear()

    def is_striking(self):
        if self.strikeD or self.strikeU:
            return True
        else:
            return False


class Racket:

    def __init__(self, player, width, height, posX, posY):
        self.player = player
        self.width = width
        self.height = height
        self.posX = posX
        self.posY = posY
        self.x = player.x + posX
        self.y = player.y + posY
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        if self.rect is not None:
            pygame.draw.rect(win, (255, 0, 255), self.rect)

    def update(self, player, posY):
        self.x = player.x
        self.y = player.y + posY
        self.rect = (self.x, self.y, self.width, self.height)

    def disappear(self):
        self.rect = None

class Ball:

    def __init__(self, x, y, moveX, moveY, game):
        self.x = x
        self.y = y
        self.dx = moveX
        self.dy = moveY
        self.game = game
        self.height = 40
        self.width = 40
        self.rectangle = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), self.rectangle)

    def update(self, game):
        self.game = game
        self.x += self.dx
        self.y += self.dy
        if self.y + self.height > 500:
            self.dy *= -1
        elif self.y < 0:
            self.dy *= -1

        # If hit
        if intersects(self, game.p1.racket):
            self.x += game.p1.racket.width
            self.dx *= -1

        if intersects(self, game.p2.racket):
            self.x -= -game.p2.racket.x + self.x + self.width
            self.dx *= -1

        if self.x + self.width > 1000:
            self.x = round((1000 - 30) / 2)
            self.y = round((500 - 30) / 2)
            self.game.score[0] += 15
        elif self.x < 0:
            self.x = round((1000 - 30) / 2)
            self.y = round((500 - 30) / 2)
            self.game.score[1] += 15

        self.rectangle = (self.x, self.y, self.width, self.height)
