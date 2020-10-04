import socket


# The function of this class, that is going to be responsable to connect the user to the server

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.13"
        self.port = 5555
        # Tupple to have the address
        self.addr = (self.server, self.port)
        # We will send an id to each person connected
        self.pos= self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            # We need to send info to get a response from the server
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
