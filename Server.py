import socket
from _thread import *
import sys

server = "192.168.0.13"
# The number of the port that we are gonna use
port = 5555

# Creating the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We need this try-catch to see if the port is avaliable
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Opens the port to have multiple clients connected
# If we leave it in blank, this will recieve all the clients that want to enter
s.listen(2)
print("Waiting for connection, server Started")


def read_position(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


# A way to store all the info about the positions of the clients
pos = [(0, 0), (100, 100)]


# This will be the threaded function
def threaded_client(conn, player):
    # We send data to the other part f the connection
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    # this will be receiving all the info, and decode it and encode it in a thread
    while True:
        try:
            # Position sent to us
            data = read_position(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
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
