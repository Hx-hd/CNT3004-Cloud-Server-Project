import socket
import threading


## (Not sure yet on what to use for ip and port) 
IP = ''
PORT = ''


ADDR = (IP, PORT)
def main() :
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

if __name__ == "__main__" :
    main()