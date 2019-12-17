import socket

ports = list()

def createServer(PORT):
    if PORT in ports:
        raise Exception("Port number already in use.")

    #AF_INET specifies the IPv4 address family &&
    #SOCK_STREAM specifies the TCP/IP suite.
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    PORT = int(PORT)

    #Returns hosting machine's name.
    HOST = socket.gethostname()
    ports.append(PORT)

    server.bind((HOST, PORT))
    print('Hosting from: ' + HOST + ", PORT: ", PORT)
    return server

def listenForConnection(server):
    print('Listening on port: ', server.getsockname()[1])
    server.listen(5)

    #New socket object to use for new connection.
    conn, addr = server.accept()
    print("Connected by, IP: " + addr[0] + ", PORT: ", addr[1])

    return conn

def receiveMessage(connection):
    while True:
        data = connection.recv(4096)

        if not data:
            break

        return data.decode()

def sendMessage(connection, message):
    connection.sendall(str.encode(message))
    print("Message succesfully sent." )

def closeConnection(connection, name):
    print("Closing connection: ", connection.getsockname())
    connection.close()
    print(name + " successfully closed.")

def closeServer(server, name):
    print("Shutting down server: " + name + " hosting on port: ", server.getsockname()[1])
    ports.remove(server.getsockname()[1])

    server.close()
    print("Server successfully closed.")

def display(message):
    if message.startswith('\"'):
        message = message[1: len(message)-1]

    print(message)

def show(vars):
    if len(vars.keys()) == 0:
        print('There are no initialized variables.')

    else:
        for k in vars.keys():
            print(k)

def close():
    exit()


#server1 = createServer(12345)
#connection1 = listenForConnection(server1)
#connection2 = listenForConnection(server1)

#print("Received: " + receiveMessage(connection1))
#print("Received: " + receiveMessage(connection2).decode())

#sendMessage(connection1, "Hello Moto1")
#sendMessage(connection2, "Hello Moto2")

#closeConnection(connection1)
#closeConnection(connection2)