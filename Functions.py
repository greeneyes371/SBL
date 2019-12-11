import socket

def createServer(port):
    #AF_INET specifies the IPv4 address family
    #SOCK_STREAM specifies the TCP
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    host = socket.gethostname()

    server.bind((host, int(port)))
    print('Connected to: ' + host + ", PORT : " + str(port))
    return server

def listenForConnection(server):
    server.listen(5)
    conn, addr = server.accept()

    #addr stores the local ip address and port number of server socket
    print("Connected by, IP: " + str(addr[0]) + ", PORT: " + str(addr[1]) + "\n")

    return conn

def receiveMessage(connection):
    while True:
        data = connection.recv(4096)

        if not data:
            break

        return data.decode()

def sendMessage(connection, message):
    connection.sendall(str.encode(message))
    print("Message succesfully sent.\n" )

def closeConnection(connection, name):
    print("Closing connection: ", connection.getsockname())
    connection.close()
    print(name + " successfully closed.\n")

def closeServer(server, name):
    print("Shutting down server: " + name)
    server.close()
    print("Server successfully closed.\n")

def display(message):
    print(message + "\n")

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