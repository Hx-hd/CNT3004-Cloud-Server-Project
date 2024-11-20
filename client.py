import socket
import os

# Server ip and port not established yet
SERVER_IP = ''
SERVER_PORT = 4466
BUFFER_SIZE = 4096  # can edit as needed
FORMAT = 'utf-8'


def connectToServer():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print('Connected to server')
    # receive and print welcome message from server
    welcomeMessage = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    print(welcomeMessage)
    return client_socket

def login(client_socket):
    while True:
        prompt = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
        username = input(prompt)
        client_socket.send(username.encode(FORMAT))
        password = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
        client_socket.send(password.encode(FORMAT))
        response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
        print(response)
        # TODO: add cases for if user login is successful and user login failed
        # Possible Solution #1:
        if response.split(' ')[1] == "successful":
            break
        else:
            continue

def uploadFile(client_socket, filename):
    if not os.path.isfile(filename):
        print('File not found')
        return False
    # Check if file already exists on the server
    client_socket.send(f"CHECK_EXISTENCE@{os.path.basename(filename)}".encode(FORMAT))
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response == "FE":
        overwrite = input("File already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            return
    client_socket.send(f"UPLOAD@{os.path.basename(filename)}".encode(FORMAT))
    with open(filename, 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE).decode(FORMAT)
            if not data:
                break
            else:
                client_socket.send(data)
    print(f'{filename} was uploaded successfully')
                # TODO: revise uploadFile implementation with server completion


def downloadFile(client_socket, filename):
    client_socket.send(f"DOWNLOAD {filename}").encode(FORMAT)
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if not response.decode(FORMAT) == 'OK':
        print("Download failed")
        return False
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
            if not data:
                break
            else:
                file.write(data)
    print(f"{filename} was downloaded successfully")
    # TODO: revise downloadFile implementation with server completion


def deleteFile(client_socket, filename):
    # TODO: implement deleteFile
    client_socket.send(f"CHECK_EXISTENCE@{os.path.basename(filename)}".encode(FORMAT))
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response == 'FNF': # file not found
        print(f"Error: {filename} not found")
        return
    if response == "FE":
        client_socket.send(f"DELETE@{filename}".encode(FORMAT))
        response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    print(response)
    return


def viewDir(client_socket):
    # TODO: implement viewDir
    client_socket.send("DIR").encode(FORMAT)
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response == "OK" :
        print("FILES IN STORAGE:")
        while True:
            filename = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
            if not filename:
                break
            print(filename)
        return
    else:
        print("Error retrieving directory contents")
        return


def createSubfolder(client_socket, subfolder):
    client_socket.send(f"CREATE_SUBFOLDER {subfolder}".encode(FORMAT))
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response == 'OK':
        print(f"{subfolder} created successfully")
    else:
        print(f"Error: creation of subfolder {subfolder} failed")
    # TODO: revise createSubfolder implementation with server completion


def deleteSubfolder(client_socket, subfolder):
    client_socket.send(f"DELETE_SUBFOLDER {subfolder}").encode(FORMAT)
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response == 'SNF':  # subfolder not found
        print(f"{subfolder} is not found")
    # possibly will not need SIP response
    elif response == 'SIP':  # subfolder in processing
        print(f"{subfolder} is being processed right now")
    elif response == 'OK':
        print(f"{subfolder} was deleted")
    else:
        print(f"Error: {subfolder} was not deleted")
    # TODO: revise deleteSubfolder implementation with server completion


def main():
    # establish connection
    client = connectToServer()
    # login user
    login(client)

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