import pandas as pd
import json
import csv
from datetime import datetime
from pythonping import ping

class DeviceAvailabilityMonitoring:
    """
    Class to monitor device availability and store the data in a CSV file.
    """
    
    def __init__(self) -> None:
        """
        Constructor to initialize the class with an empty DataFrame.
        """
        self.data: pd.DataFrame = pd.DataFrame()
    
    def file_exist(self, file: str) -> bool:
        """
        Check if a file exists.
        
        Parameters:
            file (str): The path to the file to check.
        
        Returns:
            bool: True if the file exists, False otherwise.
        """
        try:
            with open(str(file), "r"):
                return True
        except FileNotFoundError:
            return False
    
    def read_json(self) -> None:
        """
        Read data from a JSON file and store it in the DataFrame.
        """
        if not self.file_exist("device_data.json"):
            with open("device_data.json", "w") as f:
                json.dump({}, f)
        
        df = pd.read_json('device_data.json').T
        self.data = df
    
    def write_json(self) -> None:
        """
        Write data from the DataFrame to a JSON file.
        """
        if not self.file_exist("device_data.json"):
            with open("device_data.json", "w") as f:
                json.dump({}, f)
        
        self.data.T.to_json("device_data.json")
    
    def write_csv(self, device_data: list[list[str]]) -> None:
        """
        Write device availability data to a CSV file.
        
        Parameters:
            device_data (list[list[str]]): A list of lists containing device data with columns 'device_id', 'status', and 'Timestamp'.
        """
        file_exists = self.file_exist("availability_data.csv")
        
        with open("availability_data.csv", "a", newline="") as f:
            writer = csv.writer(f)
            
            if not file_exists:
                writer.writerow(["device_id", "status", "Timestamp"])
            
            for device in device_data:
                writer.writerow(device)
    
    def ping_device(self, ip: str) -> int:
        """
        Ping the specified IP address and return 1 if successful, 0 otherwise.
        
        Parameters:
            ip (str): The IP address of the device to ping.
        
        Returns:
            int: 1 if ping is successful, 0 otherwise.
        """
        try:
            response = ping(ip, verbose=False, count=1)
            if "Request timed out" in str(response):
                return 0
            else:
                return 1                
        except:
            print(ip, "is Wrong IP Address.")
            return 0
    
    def ping_devices(self) -> None:
        """
        Ping all devices in the DataFrame and store the results in a CSV file.
        """
        self.read_json()
        device_data = []
        for device_id in self.data.index:
            status = self.ping_device(self.data['ip'][device_id])
            device_data.append([device_id, status, datetime.now()])
        self.write_csv(device_data)
    
    def list_devices(self) -> None:
        """
        List all devices in the DataFrame.
        """
        self.read_json()
        print(self.data)
    
    def add_device(self) -> None:        
        """
        Add a new device to the DataFrame and save it to the JSON file.
        """
        self.read_json()
        try:
            device_id = int(input("Enter id of device: "))
        except:
            print("Device id must be integer.")
            return
        name = input("Enter name of device: ")
        ip = input("Enter ip address of device: ")
        if not device_id in self.data.index:        
            self.data.loc[device_id] = [name, ip]
            self.write_json()
            print("Device added successfully.")
        else:
            print("Device with this id already exists.")
    
    def delete_device(self, device_id: int) -> None:
        """
        Delete a device from the DataFrame and save the updated DataFrame to the JSON file.
        
        Parameters:
            device_id (int): The ID of the device to delete.
        """
        self.read_json()
        if not device_id in self.data.index:
            print("Device Not Exist.")
        else:
            self.data = self.data.drop(device_id)
            self.write_json()
            print("Device deleted successfully.")
    
    def edit_device(self, device_id: int) -> None:
        """
        Edit a device's information in the DataFrame and save the updated DataFrame to the JSON file.
        
        Parameters:
            device_id (int): The ID of the device to edit.
        """
        self.read_json()
        if not device_id in self.data.index:
            print("Device Not Exist.")
        else:
            name = input("Enter name of device: ")
            ip = input("Enter ip address of device: ")
            self.data.loc[device_id] = [name, ip]
            self.write_json()
            print("Device edited successfully.")
