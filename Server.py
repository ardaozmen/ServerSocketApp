import socket
import datetime
import time

PlaceHolder = {'userName': b'CMPE322\r\n', 'passWord': b'bilgiuni\r\n', b'date\r\n': 'get_date()', b'time\r\n':'get_time()', b'quit\r\n': 'quit()', b'capTurkey\r\n': 'get_Capital()' }
# place holder object for a database simulation which holds user informations

CONT = False # login checker

# Returns comparison results of login informations
def check_credit(userName, passWord):
    return PlaceHolder['userName'] == userName, PlaceHolder['passWord'] == passWord
def send(byte):
    to_bytes = 'b"{}"'
    clientConnection.sendall(eval(to_bytes.format(byte)))
def rec():
    data = clientConnection.recv(1024)
    try:
        data = data.replace('\r', '')
        data = data.replace('\n', '')
    except Exception as e:
        print(e)
    print(data)
    return  data
def login(client):
    global CONT
    print('starting login process')
    time.sleep(0.5)
    send('Enter your username: ')
    userName = rec()
    send('Enter your password: ')
    passWord = rec()
    _ , __ = check_credit(userName, passWord)
    if _ and __:
        time.sleep(0.5)
        send('Welcome. You are OK to ask me date, time, capTurkey, quit..')
        clientConnection.sendall(b'\n') 
        CONT = True
    else:
        send('False')
        time.sleep(0.5)
        send('Password incorrect, would you like to try the username and password again?y/n:')
        if client.recv(1024) == b'y':
            login(client)
        else:
            send('close')
            time.sleep(0.5)
            send('Thank you for trying to login, goodbye..')
            client.close()
            
def get_date():
    now = datetime.datetime.now().strftime("%Y.%m.%d -- %H:%M:%S")
    send("Current Date-Time: {}".format(now))
    clientConnection.sendall(b'\n') 
def get_time():
     now = datetime.datetime.now().strftime("%Y.%m.%d -- %H:%M:%S")
     send("Current Time:{}".format(now.split('--')[-1]))  
     clientConnection.sendall(b'\n') 
def get_Capital():
    send('Ankara')
    clientConnection.sendall(b'\n') 
def quit():
    send("bye bye...")
    clientConnection.sendall(b'\n') 
    time.sleep(0.2)
    time.sleep(0.5)
    clientConnection.sendall(b'\n') 
    client.close()     

# take the server name and port name
LOCALHOST = '0.0.0.0'
PORT = 555

# create a socket at server side using TCP / IP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket with server and port number 
server.bind((LOCALHOST, PORT))

# allow maximum 100 connection to the socket
server.listen(100)

print("Server started")
print("Waiting for client request..")

# wait till a client accept connection
clientConnection,clientAddress = server.accept()
				
# display client address
print("Connected client:" , str(clientAddress))

login(clientConnection)
while CONT:
    send('Please enter your command: ')
    data = clientConnection.recv(1024)
    
    print(data.decode())
    eval(PlaceHolder[data])
    time.sleep(0.5)