import socket
import os

# Server ip and port not established yet
SERVER_IP = ''
SERVER_PORT = ''
BUFFER_SIZE = 4096  # can edit as needed
FORMAT = 'utf-8'


def connectToServer():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print('Connected to server')
    welcomeMessage = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    print(welcomeMessage)
    return client_socket


def uploadFile(client_socket, filename):
    if not os.path.isfile(filename):
        print('File not found')
        return False
    else:
        client_socket.send(f"UPLOAD {filename}").encode(FORMAT)
        with open(filename, 'rb') as file:
            while True:
                data = file.read(BUFFER_SIZE).decode(FORMAT)
                if not data:
                    break
                else:
                    client_socket.send(data)
        print('File uploaded')
                # TODO: revise uploadFile implementation with server completion


def downloadFile(client_socket, filename):
    client_socket.send(f"DOWNLOAD {filename}")
    response = client_socket.recv(BUFFER_SIZE)
    if not response.decode(FORMAT) == 'OK':
        print("Download failed")
        return False
    if response.decode(FORMAT) == 'OK':
        with open(filename, 'wb') as file:
            while True:
                data = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
                if not data:
                    break
                else:
                    file.write(data)
        print('File downloaded')
    # TODO: revise downloadFile implementation with server completion


def deleteFile(client_socket, filename):
    client_socket.send(f"DELETE {filename}").encode(FORMAT)
    # TODO: implement deleteFile


def viewDir(client_socket):
    client_socket.send(f"VIEWDIR").encode(FORMAT)
    # TODO: implement viewDir


def createSubfolder(client_socket, subfolder):
    client_socket.send(f"CREATE SUBFOLDER {subfolder}").encode(FORMAT)
    # TODO: implement createSubfolder


def deleteSubfolder(client_socket, subfolder):
    client_socket.send(f"DELETE SUBFOLDER {subfolder}").encode(FORMAT)
    # TODO: implement deleteSubfolder

def main():
    # establish connection
    client = connectToServer()

    # prompt client with given command options
    while True:
        userInput = input("Enter a command:\n\tupload (filename)- upload file\n\tdownload (filename)- download file"
                          "\n\tdelete (filename)- delete file\n\tdir - view files/subdirectories in file storage path"
                          "\n\tcreate subfolder (subfolder name) - create subfolder"
                          "\n\tdelete subfolder (subfolder name) - delete subfolder\n\texit - exit program\n")

        # Exit
        if userInput == "exit" or userInput == "Exit":
            break

        # Upload
        elif userInput.startswith("upload") or userInput.startswith("Upload"):
            filename = userInput.split(" ")[1]
            uploadFile(client, filename)

        # Download
        elif userInput.startswith("download") or userInput.startswith("Download"):
            filename = userInput.split(" ")[1]
            downloadFile(client, filename)

        # Dir
        elif userInput == "dir" or userInput == "Dir":
            viewDir(client)

        # Delete file/subfolder
        elif userInput.startswith("delete") or userInput.startswith("Delete"):
            if userInput.split(" ")[1] == "subfolder" or userInput.split(" ")[1] == "Subfolder":
                subfolder = userInput.split(" ")[1]
                deleteSubfolder(client, subfolder)
            filename = userInput.split(" ")[1]
            deleteFile(client, filename)

        # Create subfolder
        elif userInput.startswith("create") or userInput.startswith("Create"):
            subfolder = userInput.split(" ")[1]
            createSubfolder(client, subfolder)

        # Invalid response handling
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()