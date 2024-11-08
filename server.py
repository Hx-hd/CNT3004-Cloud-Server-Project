import os
import socket
import threading


## (Not sure yet on what to use for ip and port) 
IP = socket.gethostbyname(socket.gethostname())
PORT = ''
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
        if cmd == "HELP" :
            send_data = "OK@"
            send_data += "LIST: List all files in the server directory. \n"
            send_data += "UPLOAD <path>: Upload files to the server. \n"
            send_data += "DELETE <path>: List all files from the server. \n"
            send_data += "LOGOUT: Disconnect from the server. \n"

            conn.send(send_data.encode(FORMAT))

        if cmd == DISCONNECT_MSG:
            print(f"[DISCONNECTED] {addr} disconnected. ")
            break

        print(f"[{addr} {msg}]")
        msg = f"Msg received: {msg}"
        conn.send(msg.encode(FORMAT))

    conn.close()

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