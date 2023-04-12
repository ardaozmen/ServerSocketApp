import time
import socket
import threading

class Client:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        # connect to the server
        self.client_socket.connect((self.host, self.port))
        self.connected = True
        # send username to server
        self.client_socket.send(self.username.encode())

        # start listening for messages from the server
        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    raise Exception("Connection closed by server")
                print(message)
            except:
                print("Connection closed")
                self.client_socket.close()
                self.connected = False

    def send_message(self, message):
        # send message to server
        self.client_socket.send(message.encode())

    def disconnect(self):
        # disconnect from the server
        self.client_socket.close()
        self.connected = False


if __name__ == "__main__":
    Client().connect()

    time.sleep(15)
