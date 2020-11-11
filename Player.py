import pygame
import time


class Player:

    def __init__(self, x, y, color, id):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 100
        self.color = color
        self.id = id
        self.rect = (x, y, self.width, self.height)
        self.vel = 3
        self.swing = (x, y, 0, 0)
        self.racket = Racket(self, 7, 40, 0, -40)

        # Strike booleans
        self.strikeU = False
        self.strikeD = False

        self.timer = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        if self.is_striking():
            self.racket.draw(win)

    def move(self):
        # We get all the keys that are pressed in the moment
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
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
        if self.strikeD:
            self.racket.update(self, self.height)

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
        pygame.draw.rect(win, (255, 0, 255), self.rect)

    def update(self, player, posY):
        self.x = player.x
        self.y = player.y + posY
        self.rect = (self.x, self.y, self.width, self.height)


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
        

        if self.x + self.width > 1000:
            self.x = round((1000 - 30) / 2)
            self.y = round((500 - 30) / 2)
        elif self.x < 0:
            self.x = round((1000 - 30) / 2)
            self.y = round((500 - 30) / 2)

        self.rectangle = (self.x, self.y, self.width, self.height)
