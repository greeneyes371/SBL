import socket


def createServer(port):
    server = socket.socket()
    host = socket.gethostname()

    server.bind((host, port))
    return server

def listenForConnection(server):
    server.listen(5)
    conn, addr = server.accept()
    print("Connected to " + addr)
    return conn

def PRINT(message):
    print(message)

def SHOWVARS(vars):
    if len(vars.keys()) == 0:
        print('There are no initialized variables.')

    else:
        for k,v in vars.items():
            print(k + ' == ' + v)

def EXIT(opt):
    exit()