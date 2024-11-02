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


def uploadFile(client_socket, filename):
    print("")  # temporary error-from-no-code prevention
    # TODO: implement uploadFile


def downloadFile(client_socket, filename):
    print("")  # temporary error-from-no-code prevention
    # TODO: implement downloadFile


def deleteFile(client_socket, filename):
    print("")  # temporary error-from-no-code prevention
    # TODO: implement deleteFile


def viewDir():
    print("")  # temporary error-from-no-code prevention
    # TODO: implement viewDir


def createSubfolder(client_socket, subfolder):
    print("")  # temporary error-from-no-code prevention
    # TODO: implement createSubfolder


def deleteSubfolder(client_socket, subfolder):
    print("")  # temporary error-from-no-code prevention
    # TODO: implement deleteSubfolder
