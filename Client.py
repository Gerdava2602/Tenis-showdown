import pygame
from network import Network
from Player import Player

# Creating a window
Wwidth = 1000
Wheight = 500
win = pygame.display.set_mode((Wwidth, Wheight))
pygame.display.set_caption("Tenis showdown")
icon = pygame.image.load("images\\tenis.png")
pygame.display.set_icon(icon)


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
    p = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p)
        # Something used by pygame to recieve when the program stops
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redrawWindow(win, p, p2)



main()
