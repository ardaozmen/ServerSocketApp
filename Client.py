import socket
# take the server name and port name
PlaceHolder = ['login', 'process', 'close']
def send(byte):
    to_bytes = 'b"{}"'
    client.sendall(eval(to_bytes.format(byte))) 
def rec():
    return client.recv(1024)
def login():
    print("Welcome")
    data = input(client.recv(1024).decode())
    send(data) # username info
    data = input(client.recv(1024).decode())
    send(data) # password info
    
    if client.recv(1024) == b'True\r\n':
        print(client.recv(1024).decode())
        return
    else:
        re = client.recv(1024).decode()
        server = input(re)
        send(server) # is user willing to contuniue?
        return

def close():
    print(client.recv(1024).decode())
    client.close()
    global CONT
    CONT = False
CONT = True
SERVER = '0.0.0.0'
PORT = 555

# create a socket at client side using TCP / IP protocol 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect it to server and port number on local computer.
client.connect((SERVER, PORT))

while CONT:
  retrived = rec()
  if retrived == b'login':
    login()
  elif retrived == b'close':
    close()
  else:
    cm = input('Enter your command from system: ')
    send(cm)
    print(rec().decode())