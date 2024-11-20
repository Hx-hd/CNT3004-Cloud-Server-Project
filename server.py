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


def handle_client(conn, addr) :
    print(f"[NEW CONNECTION] {addr} connected")
    conn.send("OK@Welcome to the File Server.").encode(FORMAT)

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
            else:
                conn.send("File not found".encode(FORMAT))  # Send error response

        elif cmd == "DELETE":
            filename = data[1]
            if os.path.exists(os.path.join(STORAGE_PATH, filename)):
                os.remove(os.path.join(STORAGE_PATH, filename))
                conn.send("FILE_DELETED".encode(FORMAT))
            else:
                conn.send("FNF".encode(FORMAT))

        elif cmd == "CREATE_SUBFOLDER":
            subfolder_name = data[1]
            os.makedirs(os.path.join(STORAGE_PATH, subfolder_name), exist_ok=True)
            conn.send("SUBFOLDER_CREATED".encode(FORMAT))

        elif cmd == "DELETE_SUBFOLDER":
            subfolder_name = data[1]
            subfolder_path = os.path.join(STORAGE_PATH, subfolder_name)
            if os.path.exists(subfolder_path):
                os.rmdir(subfolder_path)
                conn.send("SUBFOLDER_DELETED".encode(FORMAT))
            else:
                conn.send("SUBFOLDER_NOT_FOUND".encode(FORMAT))

        elif cmd == DISCONNECT_MSG:
            print(f"[DISCONNECTED] {addr} disconnected. ")
            break

        # print(f"[{addr} {msg}]")
        # msg = f"Msg received: {msg}"
        # conn.send(msg.encode(FORMAT))

    conn.close()

#Hash password function for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#User Authentication
def authenticate_user(conn):
    conn.send("USER@Please enter your username:".encode(FORMAT))
    username = conn.recv(SIZE).decode(FORMAT).strip()
    conn.send("PASS@Please enter your password:".encode(FORMAT))
    password = conn.recv(SIZE).decode(FORMAT).strip()
    hashed_password = hash_password(password)
    with open("users.json", "r") as f:
        users = json.load(f)
    if username in users and users[username] == hashed_password:
        conn.send(("OK@Authentication successful.".encode(FORMAT)))
        return True
    else:
        conn.send(("ERR@Authentication failed.".encode(FORMAT)))
        return False
def main() :
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True :
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__" :
    main()