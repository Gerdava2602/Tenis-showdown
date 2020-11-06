import socket
#Allows to serialize objects to send it
import pickle

# The function of this class, that is going to be responsable to connect the user to the server

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.27"
        self.port = 5555
        # Tupple to have the address
        self.addr = (self.server, self.port)
        # We will send an id to each person connected
        self.p= self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            # We need to send info to get a response from the server
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
