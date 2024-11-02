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

        # Dir
        elif userInput == "dir" or userInput == "Dir":
            viewDir()

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