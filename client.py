import socket
import os

# Server ip and port not established yet
SERVER_IP = socket.gethostbyname(socket.gethostname())
# SERVER_IP = '34.123.134.14'
# SERVER_IP = '10.128.0.2'
SERVER_PORT = 4466
BUFFER_SIZE = 4096  # can edit as needed
FORMAT = 'utf-8'


def connectToServer():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    
    # receive and print welcome message from server
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response == 'OK' :
        print('Connected to server')
        return client_socket
    

def login(client_socket):
    while True:
        client_socket.send("LOGIN".encode(FORMAT))
        prompt = client_socket.recv(BUFFER_SIZE).decode(FORMAT)  # Receive prompt from server
        print(prompt)  # Print the prompt to the user
        username = input("Enter your username: ")
        client_socket.send(username.encode(FORMAT))  # Send username to server

        prompt = client_socket.recv(BUFFER_SIZE).decode(FORMAT)  # Receive password prompt
        print(prompt)  # Print the prompt to the user
        password = input("Enter your password: ")

        client_socket.send(password.encode(FORMAT))  # Send password to server
        response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)  # Receive authentication response

        if response == "OK":
            print("Login successful!")
            break  # Exit the loop if login is successful
        else:
            print("Login failed. Please try again.")

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
    client_socket.send(f"UPLOAD@{os.path.basename(filename)}@{str(os.path.getsize(filename))}".encode(FORMAT))
    with open(filename, 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE)
            if not data:
                break
            else:
                client_socket.send(data)
    print(f'{filename} was uploaded successfully')
                # TODO: revise uploadFile implementation with server completion


def downloadFile(client_socket, filename):
    client_socket.send(f"DOWNLOAD@{filename}".encode(FORMAT))
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)

    if response != 'OK':
        print("Download failed")
        return False
    
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if data == b"EOF":  # Check for EOF message
                break
                           
            file.write(data)
    print(f"{filename} was downloaded successfully")
    # TODO: revise downloadFile implementation with server completion


def deleteFile(client_socket, filename):
    # TODO: implement deleteFile
    client_socket.send(f"CHECK_EXISTENCE@{os.path.basename(filename)}".encode(FORMAT))
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response == "FNF":
        print("Error: File not found")
        return
    
    if response == "FE":
        client_socket.send(f"DELETE@{filename}".encode(FORMAT))
        response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
        if response == "OK":
            print("File deleted successfully")
    return


def viewDir(client_socket):
    # TODO: implement viewDir
    client_socket.send("DIR".encode(FORMAT))
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
    client_socket.send(f"CREATE_SUBFOLDER@{subfolder}".encode(FORMAT))
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response == 'OK':
        print(f"Subfolder {subfolder} created successfully")
    else:
        print(f"Error: creation of subfolder {subfolder} failed")
    # TODO: revise createSubfolder implementation with server completion


def deleteSubfolder(client_socket, subfolder):
    client_socket.send(f"DELETE_SUBFOLDER@{subfolder}".encode(FORMAT))
    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response == 'SNF':  # subfolder not found
        print(f"{subfolder} is not found")
    # possibly will not need SIP response
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
        if userInput.lower() == "exit":
            break

        # Upload
        elif userInput.lower().startswith("upload"):
            filename = userInput.split(" ")[1]
            uploadFile(client, filename)

        # Download
        elif userInput.lower().startswith("download"):
            filename = userInput.split(" ")[1]
            downloadFile(client, filename)

        # Dir
        elif userInput.lower() == "dir":
            viewDir(client)

        # Delete file/subfolder
        elif userInput.lower().startswith("delete"):

            if userInput.split(" ")[1].lower() == "subfolder":
                subfolder = userInput.split(" ")[2]
                deleteSubfolder(client, subfolder)
            else:
                filename = userInput.split(" ")[1]
                deleteFile(client, filename)

        # Create subfolder
        elif userInput.lower().startswith("create"):
            subfolder = userInput.split(" ")[2]
            createSubfolder(client, subfolder)

        # Invalid response handling
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()