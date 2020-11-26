import socket
# Librería, integrada en Python, encargada de serializar objetos
import pickle


class Network:
    """
    Se encarga de conectar el cliente con el servidor a partir de la dirección
    """
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        # Enviará un ID a cada uno de los clientes
        self.p = self.connect()

    def getP(self):
        """
        Se encarga de enviar el objeto obtenido al conectar con el servidor
        :return: Object
        """
        return self.p

    def connect(self):
        """
        Conecta el objeto con el servidor y envía su dirección
        :return: Retorna un Object enviado por el servidor
        """
        try:
            self.client.connect(self.addr)
            # We need to send info to get a response from the server
            return pickle.loads(self.client.recv(2048))
        except:
            print("Error al conectarse")

    def send(self, data):
        """
        Envía la información suministrada y recibe la información de Server
        :param data: Información a enviar
        :return: Retorna un Object enviado por el servidor
        """
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
