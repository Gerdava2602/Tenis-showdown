import pygame


class Player():

    def __init__(self, x, y, width, height, color, id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3
        self.id = id
        self.swing = (x, y, 0, 0)
        self.racket = Racket(self, 30, 30)
        self.strike = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        if self.is_striking():
            self.racket.draw(win)
            print("Se pintó")

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
            self.strike = True
            print("Strike")
        else:
            self.strike = False
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
        self.racket.update(self)

    def is_striking(self):
        return self.strike


class Racket:

    def __init__(self, player, width, height):
        self.player = player
        self.x = player.x
        self.y = player.y - 40
        self.width = width
        self.height = height

        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 255), self.rect)

    def update(self,player):
        self.rect = (player.x, player.y-40, self.width, self.height)


class Ball:

    def __init__(self, x, y, moveX, moveY):
        self.x = x
        self.y = y
        self.dx = moveX
        self.dy = moveY

        self.rectangle = (x, y, 40, 40)
