import socket
from _thread import *
from Player import Player
import pickle
import sys

server = "192.168.0.27"
# The number of the port that we are gonna use
port = 5555

# Creating the socket s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We need this try-catch to see if the port is avaliable
try:
    # "une" un socket a una dirección; de lo contrario, no sabe qué dirección (par de dirección IP/puerto) debe escuchar.
    s.bind((server, port))
except socket.error as e:
    str(e)

# Opens the port to have multiple clients connected
# If we leave it in blank, this will recieve all the clients that want to enter
s.listen(2)
print("Waiting for connection, server Started")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 255, 0))]


# This will be the threaded function
def threaded_client(conn, player):
    # We are gonna send the initial player object, this will send the object
    conn.send(pickle.dumps(players[player]))
    reply = ""
    # this will be receiving all the info, and decode it and encode it in a thread
    while True:
        try:
            # Position sent to us
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    # We close the connection to be able to re-open it in the future
    conn.close()


# Number of players connected
currentPlayer = 0

# This while will browse for connections
while True:
    # This will store the connection in addr and accept the incoming requests
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
