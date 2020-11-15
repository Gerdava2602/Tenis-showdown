import pygame
from network import Network
from Player import Player

pygame.font.init()
# Creating a window
Wwidth = 1000
Wheight = 500
# win = pygame.display.set_mode((Wwidth, Wheight))

win = pygame.display.set_mode((667, Wheight))

pygame.display.set_caption("Tenis showdown")
icon = pygame.image.load("images\\tenis.png")
pygame.display.set_icon(icon)


class Button:
    def __init__(self, text, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(self.height / 2),
                        self.y + round(self.height / 2) - round(self.height / 2)))


    def click(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        else:
            return False


# Function to redraw the window
def redrawWindow(win, game):
    win.fill((255, 255, 255))
    if game is not None:
        if not game.connected():
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render("Waiting for player...", 1, (255, 0, 0), True)
            win.blit(text, (Wwidth / 2 - text.get_width() / 2, Wheight / 2 - text.get_height() / 2))
        else:
            game.draw(win)
            print(game.ball.x, game.ball.y, game.ball.m, game.ball.b)

    pygame.display.update()


# btns = [Button("Play", 100, 100, 200, 50, (0, 0, 0))]


# The function to run the main game
def main():
    global win
    win = pygame.display.set_mode((Wwidth, Wheight))

    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getP()
    game = None
    print("You are player ", player.id)

    while run:
        clock.tick(60)
        try:
            if game is None:
                game = n.send("get")
            else:
                game = n.send(player)
                player.move()
                if game == (100, 100) or game == (500, 100):
                    player.x = game[0]
                    player.y = game[1]
                    game = n.send(player)
            if not game:
                break
        except:
            run = False
            print("Couldn´t get game")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        """
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in btns:
                    if button.click(pos) and game.connected():
        """
        redrawWindow(win, game)


def draw_menu_window():
    win.fill((255, 255, 255))
    bg = pygame.image.load("images\\nadal.png")
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("Welcome to tenis showdown", 1, (255, 0, 0), True)

    win.blit(bg, (0, 0))
    win.blit(text, (667 / 2 - text.get_width() / 2, Wheight / 2 - text.get_height()))



def main_menu():
    global win
    run = True
    win = pygame.display.set_mode((667, Wheight))
    start = Button("Start", 100, 100, 100, 100, (0, 0, 0))
    exit = Button("Exit", 400, 100, 100, 100, (0, 0, 0))
    while run:

        draw_menu_window()
        start.draw()
        exit.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.click(pygame.mouse.get_pos()):
                    main()

                if exit.click(pygame.mouse.get_pos()):
                    run = False
                    pygame.quit()
        pygame.display.update()


while True:
    main_menu()
