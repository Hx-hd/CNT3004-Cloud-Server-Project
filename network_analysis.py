import time
import pandas as pd
import os


class NetworkAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame(columns=['event', 'transfer_time (sec)', 'upload_rate (MB/s)', 'download_rate (MB/s)', 'active_connections'])



    def log_metrics(self, event_type, transfer_time, upload_rate, download_rate, active_connections):
        
        new_data = {'event': event_type, 'transfer_time (sec)': transfer_time, 'upload_rate (MB/s)': upload_rate, 'download_rate (MB/s)': download_rate, 'active_connections': active_connections}
        new_data_df = pd.DataFrame([new_data])
        self.data = pd.concat([self.data, new_data_df], ignore_index=True)

        return self.data

    
    def save_metrics(self, file_path):
        self.data.to_csv(file_path, index=False)

