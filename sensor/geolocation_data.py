from data import data
from rssi import RSSI_Scan

# Function to receive closest wifi details.
def get_closest_ap():

    # Function to process and extract ssid of all the wifi's
    def getSSID(raw_cell):
        ssid = raw_cell.split('ESSID:"')[1]
        ssid = ssid.split('"')[0]
        return ssid

    # Function to process and extract mac address of all the wifi's
    def getMacAddress(raw_cell):
        mac = raw_cell.split('Address:')[1]
        mac = mac.split(' ')[1].replace("\\n", "")
        return mac

    # Function to process and extract quality of all the wifi's
    def getQuality(raw_cell):
        quality = raw_cell.split('Quality=')[1]
        quality = quality.split(' ')[0]
        return quality

    # Function to process and extract signal strength of all the wifi's
    def getSignalLevel(raw_cell):
        signal = raw_cell.split('Signal level=')[1]
        signal = int(signal.split(' ')[0])
        return signal

    # Function to parse extracted wifi details from the rssi package
    def parseCell(raw_cell):
        cell = {
            'ssid': getSSID(raw_cell),
            'quality': getQuality(raw_cell),
            'signal': getSignalLevel(raw_cell),
            'mac': getMacAddress(raw_cell)
        }
        return cell

    # Function to format extracted wifi details from the rssi package
    def formatCells(raw_cell_string):
        raw_cells = raw_cell_string.split('Cell') # Divide raw string into raw cells.
        raw_cells.pop(0) # Remove unneccesary "Scan Completed" message.
        if(len(raw_cells) > 0): # Continue execution, if atleast one network is detected.
            # Iterate through raw cells for parsing.
            # Array will hold all parsed cells as dictionaries.
            formatted_cells = [parseCell(cell) for cell in raw_cells]
            # Return array of dictionaries, containing cells.
            return formatted_cells
        else:
            print("Networks not detected.")
            return False
        
    
    obj = RSSI_Scan('wlan0')
    aps = obj.getRawNetworkScan(True)['output']
    aps = formatCells(str(aps))
    
    aps = sorted(aps, key=lambda k: k["signal"])
    closest_ap_location = {}

    for i in aps:
        if i["mac"] in data:
            closest_ap_location = data[i["mac"]]

    return closest_ap_location


print(get_closest_ap())

