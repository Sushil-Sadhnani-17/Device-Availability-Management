from device_availability_monitoring import DeviceAvailabilityMonitoring
import time
import sys

def main() -> None:
    """
    Main function to run the device availability monitoring.
    """
    device = DeviceAvailabilityMonitoring()
    
    argv_count = len(sys.argv)
    if argv_count == 1:
        while True:
            device.ping_devices()
            time.sleep(300)
    else:
        operation = sys.argv[1]
        match operation:
            case "list-devices":
                device.list_devices()
            
            case "add-device":
                device.add_device()
            
            case "delete-device":
                if argv_count < 3:
                    print("""
Wrong command line argument.
Run with "delete-device <device id>" to delete an existing device.
""")
                else:
                    try:
                        device.delete_device(int(sys.argv[2]))
                    except:
                        print("Device id must be integer.")
            
            case "edit-device":
                if argv_count < 3:
                    print("""
Wrong command line argument.
Run with "edit-device <device id>" to delete an existing device.
""")
                else:
                    try:
                        device.edit_device(int(sys.argv[2]))
                    except:
                        print("Device id must be integer.")
                
            case _:
                print("""
Wrong command line argument.
Run without any argument to check device availability.
Run with "list-devices" to list all existing devices.
Run with "add-device" to add a new device.
Run with "delete-device <device id>" to delete an existing device.
Run with "edit-device <device id>" to edit an existing device.
""")

if __name__ == "__main__":
    main()