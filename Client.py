import pygame
from network import Network

# Creating a window
Wwidth = 500
Wheight = 500
win = pygame.display.set_mode((Wwidth, Wheight))
pygame.display.set_caption("Client")

clientNumber = 0


class Player:

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

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
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_position(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


# Function to redraw the window
def redrawWindow(win, player, player2):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


# The function to run the main game
def main():
    run = True
    # Connects to the server
    n = Network()
    startPos = read_position(n.getPos())
    p = Player(startPos[0], startPos[1], 100, 50, (0, 255, 0))
    p2 = Player(0, 0, 100, 50, (255, 0, 0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = read_position(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        # Something used by pygame to recieve when the program stops
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redrawWindow(win, p, p2)


main()
