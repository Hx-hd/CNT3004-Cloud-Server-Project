import os
import socket
import threading
import hashlib
import json
import time

## (Not sure yet on what to use for ip and port) 
IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
STORAGE_PATH = "./server_storage"
DISCONNECT_MSG = "LOGOUT"

if not os.path.exists(STORAGE_PATH):

    os.makedirs(STORAGE_PATH)


def authenticate_user(conn):

    conn.send("USERNAME".encode(FORMAT))
    username = conn.recv(SIZE).decode(FORMAT).strip()
    conn.send("PASSWORD".encode(FORMAT))
    password = conn.recv(SIZE).decode(FORMAT).strip()
    hashed_password = hash_password(password)

    # Load users from JSON file
    with open("users.json", "r") as f:
        users = json.load(f)

    if username in users and users[username] == hashed_password:
        conn.send("OK".encode(FORMAT))
        return True
    else:
        conn.send("ERR".encode(FORMAT))
        return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def handle_client(conn, addr) :
    print(f"[NEW CONNECTION] {addr} connected")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    # Allow multiple authentication attempts
    authenticated = False

    while not authenticated:
        authenticated = authenticate_user(conn)

        if not authenticated:
            print(f"[DISCONNECTED] {addr} failed to authenticate.")
            conn.send("Authentication failed. Disconnecting...".encode(FORMAT))
            conn.close()  # Close connection if authentication fails

            return

    connected = True
    while connected :
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        if cmd == "CHECK_EXISTENCE":
            filename = data[1]
            if os.path.exists(os.path.join(STORAGE_PATH, filename)):
                conn.send("FE".encode(FORMAT))
            else:
                conn.send("FNF".encode(FORMAT))

        elif cmd == "DIR":
            conn.send("OK".encode(FORMAT))
            def viewDir(content, n):
                send_data = ""
                n += 1
                dirList = os.listdir(content)
                if dirList == []:
                    return
                
                for dir in dirList:
                    send_data = '\t'*n + dir
                    conn.send(send_data.encode(FORMAT))
                    print(send_data)
                    if os.path.isdir(dir) == True:
                        viewDir(dir, n)
            
            viewDir(STORAGE_PATH, -1)

        elif cmd == "UPLOAD":
            filename = data[1]
            with open(os.path.join(STORAGE_PATH, filename), 'wb') as file:
                while True:
                    data = conn.recv(SIZE)
                    if not data:
                        break
                    file.write(data)
            conn.send("UPLOAD_SUCCESSFUL".encode(FORMAT))

        elif cmd == "DOWNLOAD":
            filename = data[1]
            filepath = os.path.join(STORAGE_PATH, filename)
            if os.path.isfile(filepath):
                conn.send("OK".encode(FORMAT))  # Send OK response
                with open(filepath, 'rb') as file:
                    while True:
                        data = file.read(SIZE)
                        if not data:
                            break
                        conn.send(data)  # Send file data
                print(f"[INFO] {filename} has been sent to {addr}.")
                conn.send(b"EOF")  # Indicate end of file transfer

            else:
                conn.send("File not found".encode(FORMAT))  # Send error response

        elif cmd == "DELETE":
            filename = data[1]
            if os.path.exists(os.path.join(STORAGE_PATH, filename)):
                os.remove(os.path.join(STORAGE_PATH, filename))
                conn.send("OK".encode(FORMAT))
            else:
                conn.send("FNF".encode(FORMAT))

        elif cmd == "CREATE_SUBFOLDER":
            subfolder_name = data[1]
            os.makedirs(os.path.join(STORAGE_PATH, subfolder_name), exist_ok=True)
            conn.send("OK".encode(FORMAT))

        elif cmd == "DELETE_SUBFOLDER":
            subfolder_name = data[1]
            subfolder_path = os.path.join(STORAGE_PATH, subfolder_name)
            if os.path.exists(subfolder_path):
                os.rmdir(subfolder_path)
                conn.send("OK".encode(FORMAT))
            else:
                conn.send("SNF".encode(FORMAT))

        elif cmd == DISCONNECT_MSG:
            print(f"[DISCONNECTED] {addr} disconnected. ")
            break

        # print(f"[{addr} {msg}]")
        # msg = f"Msg received: {msg}"
        # conn.send(msg.encode(FORMAT))

    conn.close()

#Hash password function for security


def main() :

    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()  # Accept a new connection
        print(f"[NEW CONNECTION] {addr} connected")      
        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__" :
    main()