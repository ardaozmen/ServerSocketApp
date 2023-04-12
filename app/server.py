import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

    def login(self, client_socket, client_address):
        # authenticate client and add them to list of clients
        client_socket.send(b"Welcome to the server. Please enter your username: ")
        username = client_socket.recv(1024).decode().strip()
        self.clients[client_address] = username
        print(f"{username} connected from {client_address}")

    def start(self):
        # bind the socket to a public host and port
        self.server_socket.bind((self.host, self.port))
        # queue up to 5 requests
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}...")

        while True:
            # establish a connection
            client_socket, client_address = self.server_socket.accept()
            # handle client login
            threading.Thread(target=self.login, args=(client_socket, client_address)).start()

    def run(self, client_socket, client_address):
        # handle client requests
        username = self.clients[client_address]
        while True:
            try:
                message = client_socket.recv(1024).decode().strip()
                if not message:
                    raise Exception("Connection closed by client")
                print(f"{username}: {message}")
                # send message to all clients except the sender
                for address, name in self.clients.items():
                    if address != client_address:
                        message_to_send = f"{username}: {message}".encode()
                        address_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        address_socket.connect(address)
                        address_socket.send(message_to_send)
                        address_socket.close()
            except:
                print(f"{username} disconnected from {client_address}")
                del self.clients[client_address]
                client_socket.close()
                break


if __name__ == "__main__":
    Server().start()