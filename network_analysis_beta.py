import time
import pandas as pd
import socket
import matplotlib.pyplot as plt

# SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_IP = '10.128.0.2'
SERVER_PORT = 4466
BUFFER_SIZE = 4096  # can edit as needed
FORMAT = 'utf-8'

class NetworkAnalyzer:
    def __init__(self):
        self.stats = {
            "operation": [],
            "filename": [],
            "start_time": [],
            "end_time": [],
            "time_elapsed": [],
            "file_size": [],
            "data_rate": [],
            "response_time": [],
            "upload_rate": [],
            "download_rate":[],
        }

    def connect_to_server(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))  # Connect to the server
        print(f"Connected to server at {host}:{port}")

    def login(self, host, port):
        while True:
            # Code only works if i catch the prompt. prompt not needed to show for NetA
            prompt = self.socket.recv(BUFFER_SIZE).decode(FORMAT)
            self.socket.send('neta'.encode(FORMAT))  # user = neta
            prompt = self.socket.recv(BUFFER_SIZE).decode(FORMAT)  # catch 2nd prompt
            self.socket.send('authorize'.encode(FORMAT))  # password = authorize
            response = self.socket.recv(BUFFER_SIZE).decode(FORMAT)  # Receive authentication response
            if response == "OK":
                print("NetworkAnalysis: AUTHENTICATED")
                break  # move on to next step if auth. works
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

    def start_timer(self):
        #Starts the timer
        return time.time()

    def upload_data(self, data, filename=""):
        start_time = time.time()
        self.socket.sendall(data)
        end_time = time.time()

        time_elapsed = end_time - start_time
        upload_rate = len(data) / time_elapsed if time_elapsed > 0 else 0

        self.end_timer(start_time, "upload", filename=filename, file_size=len(data), time_elapsed=time_elapsed)
        print(f"Upload rate: {upload_rate:.2f} bytes/second")
        return upload_rate

    def download_data(self, expected_size, filename=""):
        received_data = b""
        start_time = time.time()
        while len(received_data) < expected_size:
            chunk = self.socket.recv(BUFFER_SIZE)
            if not chunk:
                break
            received_data += chunk
        end_time = time.time()

        time_elapsed = end_time - start_time
        download_rate = len(received_data) / time_elapsed if time_elapsed > 0 else 0

        self.end_timer(start_time, "download", filename=filename, file_size=len(received_data),
                       time_elapsed=time_elapsed)
        print(f"Download rate: {download_rate:.2f} bytes/second")
        return download_rate

    def end_timer(self, start_time, operation, filename="", file_size=0, time_elapsed=0, response_time=0):
        end_time = time.time()
        data_rate = file_size / time_elapsed if time_elapsed > 0 else 0

        self.stats["operation"].append(operation)
        self.stats["filename"].append(filename)
        self.stats["start_time"].append(start_time)
        self.stats["end_time"].append(end_time)
        self.stats["time_elapsed"].append(time_elapsed)
        self.stats["response_time"].append(response_time)
        self.stats["file_size"].append(file_size)
        self.stats["data_rate"].append(data_rate)
        if operation == "upload":
            self.stats["upload_rate"].append(data_rate)
        elif operation == "download":
            self.stats["download_rate"].append(data_rate)

    def measure_latency(self):
        start_time = time.time()
        self.socket.send(b"ping")
        self.socket.recv(BUFFER_SIZE)
        end_time = time.time()
        latency = end_time - start_time
        print(f"Latency: {latency:.6f} seconds")
        return latency

    def save_to_file(self, file_path):
        #Saves the stats recorded to file
        df = pd.DataFrame(self.stats)
        df.to_csv(file_path, index=False)

    def get_dataframe(self):
        #Returns each stat within a dataframe
        return pd.DataFrame(self.stats)

    def plot_rates(self):
        df = self.get_dataframe()
        upload_rates = df[df["operation"] == "upload"]["data_rate"]
        download_rates = df[df["operation"] == "download"]["data_rate"]
        operations = range(len(upload_rates))  # Assuming sequential operation IDs

        plt.figure(figsize=(10, 6))
        plt.plot(operations, upload_rates, label="Upload Rates", marker="o")
        plt.plot(operations, download_rates, label="Download Rates", marker="o")
        plt.xlabel("Operation Number")
        plt.ylabel("Data Rate (Bytes/Second)")
        plt.title("Upload and Download Rates")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_response_times(self):
        df = self.get_dataframe()
        plt.figure(figsize=(10, 6))
        plt.plot(df["start_time"], df["response_time"], label="Response Time", marker="o", color="green")
        plt.xlabel("Start Time")
        plt.ylabel("Response Time (Seconds)")
        plt.title("Response Times Over Operations")
        plt.legend()
        plt.grid()
        plt.show()

analyzer = NetworkAnalyzer()
analyzer.connect_to_server(SERVER_IP, SERVER_PORT)
analyzer.login(SERVER_IP, SERVER_PORT)

# Perform an upload or download operation
data = b"Insert test data"  # Insert your test data
analyzer.upload_data(data, filename="test_upload.txt") # put the test files in

# Generate plots after recording statistics
df = analyzer.get_dataframe()
analyzer.plot_rates(df)
analyzer.plot_response_times(df)
