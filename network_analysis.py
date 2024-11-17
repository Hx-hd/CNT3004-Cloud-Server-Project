import time
import pandas as pd

class NetworkAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame(columns=['event', 'transfer_time', 'upload_rate', 'download_rate', 'active_connections', 'timestamp'])

    def start_transfer(self):
        self.start_time = time.time()

    def end_transfer(self, size, event_type):
        end_time = time.time()
        transfer_time = end_time - self.start_time
        if event_type == 'upload':
            upload_rate = size / transfer_time
            download_rate = None
        elif event_type == 'download':
            download_rate = size / transfer_time
            upload_rate = None
        new_data = {'event': event_type, 'transfer_time': transfer_time, 'upload_rate': upload_rate, 'download_rate': download_rate, 'active_connections': None, 'timestamp': time.time()}
        self.data = self.data.append(new_data, ignore_index=True)

    def get_metrics(self):
        return self.data

    def save_metrics(self, file_path):
        self.data.to_csv(file_path, index=False)

    def collect_active_connections(self, active_connections):
        new_data = {'event': 'active_connections', 'transfer_time': None, 'upload_rate': None, 'download_rate': None, 'active_connections': active_connections, 'timestamp': time.time()}
        self.data = self.data.append(new_data, ignore_index=True)

if __name__ == "__main__":
    analyzer = NetworkAnalyzer()
    # Example usage:
    analyzer.start_transfer()
    time.sleep(2)  # base transfer delay, but may change
    analyzer.end_transfer(1024 * 1024 * 25, 'upload')  # Simulate 25MB file upload
    analyzer.start_transfer()
    time.sleep(3)  # Simulate another file transfer delay
    analyzer.end_transfer(1024 * 1024 * 25, 'download')  # Simulate 25MB file download
    analyzer.collect_active_connections(5)   # base transfer delay, but may change
    print(analyzer.get_metrics())
    analyzer.save_metrics("network_metrics.csv")