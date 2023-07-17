import pandas as pd
import csv
import time
from datetime import datetime
from pythonping import ping
import schedule

class DeviceAvailabilityMonitoring:
    """
    Class to monitor device availability and store the data in a CSV file.
    """
    
    def __init__(self) -> None:
        """
        Constructor to initialize the class with an empty DataFrame.
        """
        self.data: pd.DataFrame = pd.DataFrame()
    
    def read_json(self) -> None:
        """
        Read data from a JSON file and store it in the DataFrame.
        """
        df: pd.DataFrame = pd.read_json('device_data.json').T
        self.data = df
    
    def ping_device(self, ip: str) -> int:
        """
        Ping the specified IP address and return 1 if successful, 0 otherwise.
        """
        try:
            response = ping(ip, verbose=False)
            if "Request timed out" in str(response):
                return 0
            else:
                return 1                
        except:
            print(ip, "is Wrong IP Address.")
            return 0
    
    def write_csv(self, device_data: list[list[str]]) -> None:
        """
        Write device availability data to a CSV file.
        """
        file_exists = False
        try:
            with open("availability_data.csv", "r"):
                file_exists = True
        except FileNotFoundError:
            pass
        
        with open("availability_data.csv", "a", newline="") as f:
            writer = csv.writer(f)
            
            if not file_exists:
                writer.writerow(["device_id", "status", "Timestamp"])
            
            for device in device_data:
                writer.writerow(device)
    
    def ping_devices(self) -> None:
        """
        Ping all devices in the DataFrame and store the results in a CSV file.
        """
        self.read_json()
        device_data = []
        for device_name in self.data.index:
            result = [self.data['id'][device_name]]
            status = self.ping_device(self.data['ip'][device_name])
            result.extend([status, datetime.now()])
            device_data.append(result)
        self.write_csv(device_data)

def main():
    """
    Main function to run the device availability monitoring.
    """
    monitor_device = DeviceAvailabilityMonitoring()
    monitor_device.ping_devices()

if __name__ == "__main__":
    schedule.every(5).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
