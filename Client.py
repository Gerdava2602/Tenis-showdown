import pygame
from network import Network


pygame.font.init()

# Crea la ventana con las dimensiones deseadas
Wwidth = 1000
Wheight = 500
win = pygame.display.set_mode((Wwidth, Wheight))

# Define las características de la ventana
pygame.display.set_caption("Tenis showdown")
icon = pygame.image.load("images\\tenis.png")
pygame.display.set_icon(icon)

# Inicializa el reproductor de sonidos
pygame.mixer.init()


class Button:
    """
    La clase Button, es una clase creada para usarse en la GUI del Script
    """
    def __init__(self, x, y, width, height):
        """
        :param x: Posición inicial del botón con respecto al eje de las X
        :param y: Posición inicial del botón con respecto al eje de las Y
        :param width: Ancho del botón
        :param height: Altura del botón
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (self.x, self.y, self.width, self.height)

    def click(self, pos):
        """
        La función se encarga de validar si la posición coincide con los parámetros del botón
        :param pos: Una posición representada como un Tuple
        :return: Booleano, que testifica si hay una intersección o no
        """
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game):
    """
    Esta función se encarga de actualizar y dibujar la ventana en cada iteración
    :param win: La ventana creada
    :param game: El juego actual en el que se encuentra el cliente
    :return: void
    """
    win.fill((255, 255, 255))
    if game is not None:
        if not game.connected():
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render("Waiting for player...", 1, (255, 0, 0), True)
            win.blit(text, (Wwidth / 2 - text.get_width() / 2, Wheight / 2 - text.get_height() / 2))
        else:
            game.draw(win)

    pygame.display.update()


def main():
    """
    Se encarga de contener el ciclo principal del programa. Iniciará todas las funciones básicas del Client
    :return:
    """
    global win
    win = pygame.display.set_mode((Wwidth, Wheight))

    # Inicia la música característica del juego
    pygame.mixer.music.stop()
    pygame.mixer.music.load("sounds\\game.mp3")
    pygame.mixer.music.play(-1)
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getP()
    if player is None:
        return
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
                if game == (1, 218) or game == (957, 218):
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
        redrawWindow(win, game)


def draw_menu_window():
    """
    Se encarga de dibujar el menú de entrada
    :return:
    """
    win.fill((255, 255, 255))
    bg = pygame.image.load("images\\menuTenisShowdown.png")
    win.blit(bg, (0, 0))


def main_menu():
    """
    Se encarga de contener el ciclo principal del Menú
    :return:
    """
    global win
    run = True
    start = Button(311, 387, 355, 65)
    pygame.mixer.music.stop()
    pygame.mixer.music.load("sounds\\menu.ogg")
    pygame.mixer.music.play(-1)
    while run:

        draw_menu_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.click(pygame.mouse.get_pos()):
                    main()
        pygame.display.update()

# Se usa un ciclo para verificar que siempre se volverá al menú después de cualquier cierre en el juego
while True:
    main_menu()
