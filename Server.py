import socket
from _thread import *
from Player import Player
from Game import Game
import pickle
import time


# Obtiene la dirección IP actual, en la cual, funcionará el servidor
# Este obtiene la dirección IP del dispositivo
server = socket.gethostbyname(socket.gethostname())
# La dirección del puerto que va a usar
port = 5555


# Crea un socket usando dos parámetros. El primero, es el tipo de información y el segundo su categoría
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Usamos un try-catch para verificar que el puerto y el server sean útiles
try:
    # "une" un socket a una dirección; de lo contrario, no sabe qué dirección (par de dirección IP/puerto) debe
    # escuchar.
    s.bind((server, port))
except socket.error as e:
    str(e)

# Se declara el diccionario de juegos
games = {}

# Se inicializa el contador de jugadores
idCount = 0


def threaded_client(conn, p, gameId):
    """
    Esta función crea un hilo, en el cual, se realizarán todas las acciones del cliente junto su actualización
    :param conn: Conexión adquirida del método accept
    :param p: Es el ID del jugador actual
    :param gameId: ID del juego al cual pertenece el cliente
    :return: void
    """

    global idCount
    timer = 0

    # Envía el jugador en su estado inicial al cliente
    if p == 0:
        conn.send(pickle.dumps(Player(100, 250, p), p))
    else:
        conn.send(pickle.dumps(Player(900, 250, p), p))

    # Se inicializa la respuesta que será enviada posteriormente
    reply = ""

    while True:
        try:
            # Obtiene la información recibida desde el cliente
            data = pickle.loads(conn.recv(4096))

            # Valida que el ID del juego exista
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    # Resetea las posiciones y variables del juego al terminar un Game
                    if game.score[0] == 60 or game.score[1] == 60:
                        if p == 0 and not game.recieved[0]:
                            conn.send(pickle.dumps((1, 218)))
                            game.recieved[0] = True
                        elif p == 1 and not game.recieved[1]:
                            conn.send(pickle.dumps((957, 218)))
                            game.recieved[1] = True

                        # Valida que los dos jugadores reciban la información
                        if game.recieved[0] and game.recieved[1]:
                            if game.score[0] == 60:
                                game.sets.append(0)
                            elif game.score[1] == 60:
                                game.sets.append(1)
                            game.set_reset()
                            game.recieved[0] = False
                            game.recieved[1] = False

                    # Vigila que no se haya acabado el juego
                    if game.winner():

                        # Inicia el contador para el final del juego
                        if int(time.time() - start_time) > 3:
                            break
                    else:

                        # Agrega el tiempo actual por si se termina el juego
                        start_time = time.time()

                    if data != "get":

                        # Obtiene el jugador desde el cliente y lo actualiza en el juego
                        game.get_player(data, p)

                    # Actualiza el juego
                    game.update()
                    reply = game

                    # Envía la información al cliente
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")

    try:

        # Se termina la conexión y se elimina el juego del diccionario
        del games[gameId]
        print("Closing game ", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


print("[STARTING] the server is about to start...")
# Abre el puerto para recibir los clientes
s.listen()

print("Waiting for connection, server Started")

# Buscará constantemente peticiones de conexión
while True:
    # Almacenará la conexión y la dirección del cliente. Este proceso esperará hasta encontrar una conexión
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0

    # Crea IDs para los juegos dependiendo del número de jugadores
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        # Avisa al juego cuando los dos jugadores estén conectados
        games[gameId].ready = True
        p = 1

    # Inicia un hilo para la función indicada
    start_new_thread(threaded_client, (conn, p, gameId))
