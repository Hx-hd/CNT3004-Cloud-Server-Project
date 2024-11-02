import socket

# Server ip and port not established yet
SERVER_IP = ''
SERVER_PORT = ''
BUFFER_SIZE = 1024  # can edit as needed


def connectToServer():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print('Connected to server')
    return client_socket

