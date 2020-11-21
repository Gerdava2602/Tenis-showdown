import random
import pygame
import time

def intersects(first, other):
    return first.x < other[0] + other[2] and first.x + first.width > other[0] and first.y < other[1] + other[3] \
           and first.y + first.height > other[1]


# Sprite
right = [pygame.image.load("images\\Right_1.png"), pygame.image.load("images\\Right_2.png"),
         pygame.image.load("images\\Right_3.png")]
up = [pygame.image.load("images\\Up_1.png"), pygame.image.load("images\\Up_2.png"),
      pygame.image.load("images\\Up_3.png")]
left = [pygame.image.load("images\\Left_1.png"), pygame.image.load("images\\Left_2.png"),
        pygame.image.load("images\\Left_3.png")]
down = [pygame.image.load("images\\Down_1.png"), pygame.image.load("images\\Down_2.png"),
        pygame.image.load("images\\Down_3.png")]

count = 0

# Sound effects
pygame.mixer.init()

hit = pygame.mixer.Sound("sounds\\hit.wav")
swing = pygame.mixer.Sound("sounds\\swing.wav")


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
        self.racket = Racket(self, 32, 40, 0, -40)
        self.start_time = 0

        # Strike booleans
        self.strikeU = False
        self.strikeD = False
        self.can_strike = True

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
                self.y = 499 - self.height

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

        if keys[pygame.K_q] and self.can_strike:
            swing.play()
            self.strikeU = True
            self.can_strike = False
        else:
            self.strikeU = False
        if keys[pygame.K_a] and self.can_strike:
            swing.play()
            self.strikeD = True
            self.can_strike = False
        else:
            self.strikeD = False
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
        if self.can_strike:
            self.start_time = time.time()
        else:
            if int(time.time() - self.start_time) > 1:
                self.can_strike = True

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
            if self.posY == -40:
                rack = pygame.image.load("images\\tennis-racket.png")
            else:
                rack = pygame.image.load("images\\tennis-racket-downside.png")
            win.blit(rack, (self.x, self.y))

    def update(self, player, posY):
        self.x = player.x
        self.posY = posY
        self.y = player.y + posY
        self.rect = (self.x, self.y, self.width, self.height)

    def disappear(self):
        self.rect = None


class Ball:

    def __init__(self, game):
        self.game = game
        self.x = self.game.serve_points[len(self.game.sets)][0]
        self.y = self.game.serve_points[len(self.game.sets)][1]
        self.dx = 0
        self.m = 1
        self.b = 0
        self.serving = False
        self.height = 32
        self.width = 32
        self.rectangle = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        ball = pygame.image.load("images\\tenis.png")
        win.blit(ball, (self.x, self.y))

    def update(self, game):
        self.game = game

        # If hit
        if game.p1.racket.rect is not None:
            if intersects(self, game.p1.racket.rect):
                self.serving = False
                hit.play()
                if self.dx == 0:
                    self.dx = 5
                else:
                    self.dx += random.randint(-1, 1)
                    self.dx *= -1
                self.x += game.p1.racket.width
                # Y destino = y2, X destino = 1000
                # Y origen = self.y, X origen = self.x
                y2 = -1 * random.randint(1, 500 - self.height)
                self.m = (y2 - -self.y) / (1000 - self.x)
                self.b = (self.x * y2 - 1000 * -self.y) / (self.x - 1000)

        if game.p2.racket.rect is not None:
            if intersects(self, game.p2.racket.rect):
                self.serving = False
                hit.play()
                if self.dx == 0:
                    self.dx = 5
                else:
                    self.dx += random.randint(-1, 1)
                    self.dx *= -1
                self.x -= -game.p2.racket.x + self.x + self.width
                # Y origen = self.y, X origen = self.x
                # Y destino = y2, X destino = 0
                y2 = -1 * random.randint(1, 500 - self.height)
                self.m = (y2 - -self.y) / -self.x
                self.b = self.x * y2 / self.x

        if not self.serving:
            if self.m == 1:
                self.y = (self.m * self.x + self.b)
            else:
                self.y = -1 * (self.m * self.x + self.b)

        if self.x + self.width > 1000:
            self.game.score[0] += 15
            if self.game.score[0] != 60:
                self.x = self.game.serve_points[len(self.game.sets)][0]
                self.y = self.game.serve_points[len(self.game.sets)][1]
            else:
                self.x = self.game.serve_points[len(self.game.sets)+1][0]
                self.y = self.game.serve_points[len(self.game.sets)+1][1]
            self.dx = 0
            self.serving = True
        elif self.x < 0:
            self.game.score[1] += 15
            if self.game.score[1] != 60:
                self.x = self.game.serve_points[len(self.game.sets)][0]
                self.y = self.game.serve_points[len(self.game.sets)][1]
            else:
                self.x = self.game.serve_points[len(self.game.sets)+1][0]
                self.y = self.game.serve_points[len(self.game.sets)+1][1]
            self.dx = 0
            self.serving = True
        else:
            self.x += self.dx

        self.rectangle = (self.x, self.y, self.width, self.height)
