import time
import pandas as pd
import socket

# SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_IP = '10.128.0.2'
SERVER_PORT = 4466
BUFFER_SIZE = 4096  # can edit as needed
FORMAT = 'utf-8'



class NetworkAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame(columns=['event', 'transfer_time', 'upload_rate', 'download_rate', 'active_connections', 'timestamp'])
        self.server_address = None
        self.socket = None
        self.receiving_metrics = False  # Flag to indicate if we're receiving metrics

    def connect_to_server(self, host, port):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))  # Connect to the server
            print(f"Connected to server at {host}:{port}")
            
    
    def login(self,host,port):
        while True:
            # Code only works if i catch the prompt. prompt not needed to show for NetA
            prompt = self.socket.recv(BUFFER_SIZE).decode(FORMAT)
            self.socket.send('neta'.encode(FORMAT)) # user = neta
            prompt = self.socket.recv(BUFFER_SIZE).decode(FORMAT)  # catch 2nd prompt
            self.socket.send('authorize'.encode(FORMAT)) # password = authorize
            response = self.socket.recv(BUFFER_SIZE).decode(FORMAT)  # Receive authentication response
            if response == "OK":
                print("NetworkAnalysis: AUTHENTICATED")
                break #move on to next step if auth. works
            else:
                print("NetworkAnalysis: Auth. failiure")


    def wait_for_server_response(self):

        while True:
            response = self.socket.recv(BUFFER_SIZE).decode(FORMAT)
            if not response:
                break            

            # Check for specific confirmation messages
            if response == "UPLOAD_SUCCESSFUL" or response == "DOWNLOAD_SUCCESSFUL":
                self.is_receiving_metrics = True
                print("Received confirmation from server. Starting to receive metrics...")
                self.receive_metrics()
                break  # Exit the loop after starting to receive metrics

    def receive_metrics(self):

        while self.receiving_metrics:
            self.send("OK".encode(FORMAT)) 
            data = self.socket.recv(BUFFER_SIZE).decode(FORMAT)
            if not data:
                break
            # Expecting data in the format: "EVENT@TRANSFER_TIME@UPLOAD_RATE OR DOWNLOAD_RATE@ACTIVE_CONNECTIONS"
            metric_data = data.split("@")
            if len(metric_data) < 5:
                print("Received malformed data from server.")
                continue

            event = metric_data[0]
            transfer_time = float(metric_data[1])
            upload_rate = float(metric_data[2])
            download_rate = float(metric_data[3])
            active_connections = int(metric_data[4])
            new_data = pd.DataFrame({'event': [event], 
                                    'transfer_time': [transfer_time], 
                                    'upload_rate': [upload_rate], 
                                    'download_rate': [download_rate], 
                                    'active_connections': [active_connections], 
                                    'timestamp': [time.time()]})
            self.data = pd.concat([self.data, new_data], ignore_index=True)


    def get_metrics(self):
        return self.data

    def save_metrics(self, file_path):
        self.data.to_csv(file_path, index=False)

    def log_transfer(self, event, transfer_time, upload_rate, download_rate):
            new_data = {
                'event': event,
                'transfer_time': transfer_time,
                'upload_rate': upload_rate,
                'download_rate': download_rate,
                'active_connections': None,  # Placeholder for active connections
                'timestamp': time.time()
            }

            self.data = self.data.append(new_data, ignore_index=True)  # Append new data to DataFrame
    def collect_active_connections(self, active_connections):
        new_data = pd.DataFrame({'event': ['active_connections'], 
                                'transfer_time': [None], 
                                'upload_rate': [None], 
                                'download_rate': [None], 
                                'active_connections': [active_connections], 
                                'timestamp': [time.time()]})
        self.data = pd.concat([self.data, new_data], ignore_index=True)

if __name__ == "__main__":
    
    analyzer = NetworkAnalyzer()
    analyzer.connect_to_server(SERVER_IP, SERVER_PORT)
    analyzer.login(SERVER_IP, SERVER_PORT)
    analyzer.wait_for_server_response()  # Wait for server confirmation before receiving metrics
    print(analyzer.get_metrics())
    analyzer.save_metrics("network_metrics.csv")
