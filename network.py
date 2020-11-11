import socket
# Allows to serialize objects to send it
import pickle


# The function of this class, that is going to be responsable to connect the user to the server

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Public address 190.84.118.189
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        # Tupple to have the address
        self.addr = (self.server, self.port)
        # We will send an id to each person connected
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            # We need to send info to get a response from the server
            return pickle.loads(self.client.recv(2048))
        except:
            print("Error al conectarse")

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
