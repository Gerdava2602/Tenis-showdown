import socket
from _thread import *
from Player import Player
from Game import Game
import pickle
import time
import sys

# Gets the ipv4 of the host
# Public address 190.84.118.189
server = socket.gethostbyname(socket.gethostname())
# The number of the port that we are gonna use
port = 5555

# Creating the socket the first is the type of info and the second is the category of socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We need this try-catch to see if the port is avaliable
try:
    # "une" un socket a una dirección; de lo contrario, no sabe qué dirección (par de dirección IP/puerto) debe
    # escuchar.
    s.bind((server, port))
except socket.error as e:
    str(e)

games = {}
idCount = 0


# This will be the threaded function
def threaded_client(conn, p, gameId):
    global idCount
    timer = 0
    if p == 0:
        conn.send(pickle.dumps(Player(100, 250, (0, 255, 255), p), p))
    else:
        conn.send(pickle.dumps(Player(900, 250, (255, 0, 255), p), p))
    reply = ""

    while True:
        try:
            data = pickle.loads(conn.recv(4096))

            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    # Resets the game when one player won
                    if game.score[0] == 60 or game.score[1] == 60:
                        if p == 0 and not game.recieved[0]:
                            conn.send(pickle.dumps((1, 218)))
                            game.recieved[0] = True
                        elif p == 1 and not game.recieved[1]:
                            conn.send(pickle.dumps((957, 218)))
                            game.recieved[1] = True

                        if game.recieved[0] and game.recieved[1]:
                            if game.score[0] == 60:
                                game.sets.append(0)
                            elif game.score[1] == 60:
                                game.sets.append(1)
                            game.set_reset()
                            game.recieved[0] = False
                            game.recieved[1] = False

                        if game.winner():
                            if int(time.time() - start_time) > 5:
                                break
                        else:
                            start_time = time.time()

                    elif data != "get":
                        game.get_player(data, p)
                    game.update()
                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")

    try:
        del games[gameId]
        print("Closing game ", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


print("[STARTING] the server is about to start...")
# Opens the port to have multiple clients connected
# If we leave it in blank, this will recieve all the clients that want to enter
s.listen(2)

print("Waiting for connection, server Started")
# This while will browse for connections
while True:
    # This will store the connection in addr and accept the incoming requests. This will wait until new connections
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
