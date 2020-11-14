import random

import pygame
import time


def intersects(first, other):
    return first.x < other.x + other.width and first.x + first.width > other.x and first.y < other.y + other.height \
           and first.y + first.height > other.y


right = [pygame.image.load("images\\Right_1.png"), pygame.image.load("images\\Right_2.png"),
         pygame.image.load("images\\Right_3.png")]
up = [pygame.image.load("images\\Up_1.png"), pygame.image.load("images\\Up_2.png"), pygame.image.load("images\\Up_3.png")]
left = [pygame.image.load("images\\Left_1.png"), pygame.image.load("images\\Left_2.png"), pygame.image.load("images\\Left_3.png")]
down = [pygame.image.load("images\\Down_1.png"), pygame.image.load("images\\Down_2.png"), pygame.image.load("images\\Down_3.png")]

count = 0


class Player:

    def __init__(self, x, y, color, id):
        self.x = x
        self.y = y
        self.width = 42
        self.height = 62
        self.color = color
        self.id = id
        self.rect = (x, y, self.width, self.height)
        self.vel = 5
        self.swing = (x, y, 0, 0)
        self.racket = Racket(self, 7, 40, 0, -40)

        # Strike booleans
        self.strikeU = False
        self.strikeD = False

        # Move booleans
        self.right = False
        self.left = False
        self.up = False
        self.down = False

        self.counter = 1
        self.timer = 0

    def draw(self, win):

        global count

        if count + 1 >= 9:
            count = 0

        if self.up:
            win.blit(up[count // 3], (self.x, self.y))
        elif self.down:
            win.blit(down[count // 3], (self.x, self.y))
        elif self.right:
            win.blit(right[count // 3], (self.x, self.y))
        elif self.left:
            win.blit(left[count // 3], (self.x, self.y))
        else:
            if self.id == 1:
                win.blit(left[2], (self.x, self.y))
            else:
                win.blit(right[2], (self.x, self.y))
        count += 1
        if self.is_striking():
            self.racket.draw(win)

    def move(self):
        # We get all the keys that are pressed in the moment
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.right = False
            self.left = False
            self.up = True
            self.down = False
            self.y -= self.vel

            # Validations
            if self.y <= 0:
                self.y = 1
        if keys[pygame.K_DOWN]:
            self.right = False
            self.left = False
            self.up = False
            self.down = True
            self.y += self.vel

            # Validations
            if self.y + self.height >= 500:
                self.y = 499-self.height

        if keys[pygame.K_LEFT]:
            self.right = False
            self.left = True
            self.up = False
            self.down = False
            self.x -= self.vel

            # Validations
            if self.id == 1:
                if self.x <= 500:
                    self.x = 501
            else:
                if self.x <= 0:
                    self.x = 1

        if keys[pygame.K_RIGHT]:
            self.right = True
            self.left = False
            self.up = False
            self.down = False
            self.x += self.vel

            # Validations
            if self.id == 1:
                if self.x + self.width >= 1000:
                    self.x = 1000 - self.width - 1
            else:
                if self.x + self.width >= 500:
                    self.x = 500 - self.width - 1

            # Validations
            if self.y + self.height >= 500:
                self.y = 500 - self.height - 1

        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.up = False
            self.down = False
            self.left = False
            self.right = False

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
        self.rect = None

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
        self.m = 0.2
        self.b = 0
        self.height = 32
        self.width = 32
        self.rectangle = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        ball = pygame.image.load("images\\tenis.png")
        win.blit(ball, (self.x, self.y))

    def update(self, game):
        self.game = game
        self.b = 0
        self.x += self.dx
        # If hit
        if intersects(self, game.p1.racket):
            self.x += game.p1.racket.width
            y2 = random.randint(1, 500)
            self.m = (y2 - self.y) // (1000 - self.x)
            self.b = (1000*self.y - self.x*y2)//(self.x - 1000)
            self.dx *= -1

        if intersects(self, game.p2.racket):
            self.x -= -game.p2.racket.x + self.x + self.width
            y2 = random.randint(1, 500)
            self.m = (self.y - y2) // self.x
            if self.m < 0:
                self.m *= -1
            self.b = y2
            self.dx *= -1

        self.y = 500 - (500 - self.m * self.x + self.b)

        if self.x + self.width > 1000:
            self.x = round((1000 - 30) / 2)
            self.y = round((500 - 30) / 2)
            self.game.score[0] += 15
        elif self.x < 0:
            self.x = round((1000 - 30) / 2)
            self.y = round((500 - 30) / 2)
            self.game.score[1] += 15

        print(self.m, self.x, self.y)
        self.rectangle = (self.x, self.y, self.width, self.height)
