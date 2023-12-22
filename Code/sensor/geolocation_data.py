from data import data
from rssi import RSSI_Scan

## Function to receive closest wifi details.
def get_closest_ap():
    ## Function to process and extract ssid of all the wifi's
    # @param raw_cell: A string containing raw data of a single Wi-Fi access point.
    # @return The ssid extracted from the raw data.
    def getSSID(raw_cell):
        ssid = raw_cell.split('ESSID:"')[1]
        ssid = ssid.split('"')[0]
        return ssid

    ## Function to process and extract mac address of all the wifi's
    # @param raw_cell: A string containing raw data of a single Wi-Fi access point.
    # @return The MAC address extracted from the raw data.
    def getMacAddress(raw_cell):
        mac = raw_cell.split('Address:')[1]
        mac = mac.split(' ')[1].replace("\\n", "")
        return mac

    ## Function to process and extract quality of all the wifi's
    # @param raw_cell: A string containing raw data of a single Wi-Fi access point.
    # @return The quality extracted from the raw data.
    def getQuality(raw_cell):
        quality = raw_cell.split('Quality=')[1]
        quality = quality.split(' ')[0]
        return quality

    ## Function to process and extract signal strength of all the wifi's
    # @param raw_cell: A string containing raw data of a single Wi-Fi access point.
    # @return The signal level extracted from the raw data as an integer.
    def getSignalLevel(raw_cell):
        signal = raw_cell.split('Signal level=')[1]
        signal = int(signal.split(' ')[0])
        return signal

    ## Function to parse extracted wifi details from the rssi package
    # @param raw_cell: A string containing raw data of a single Wi-Fi access point.
    # @return A dictionary with ssid, quality, signal, and mac of a Wi-Fi access point.
    def parseCell(raw_cell):
        cell = {
            'ssid': getSSID(raw_cell),
            'quality': getQuality(raw_cell),
            'signal': getSignalLevel(raw_cell),
            'mac': getMacAddress(raw_cell)
        }
        return cell

    ## Function to format extracted wifi details from the rssi package
    # @param raw_cell_string: String containing the raw data from a Wi-Fi scan.
    # @return A list of dictionaries, each containing details of a Wi-Fi access point. False if no networks detected.
    def formatCells(raw_cell_string):
        raw_cells = raw_cell_string.split('Cell') # Divide raw string into raw cells.
        raw_cells.pop(0) # Remove unnecessary "Scan Completed" message.
        if(len(raw_cells) > 0): # Continue execution if at least one network is detected.
            formatted_cells = [parseCell(cell) for cell in raw_cells] # Parse each cell into a dictionary.
            return formatted_cells
        else:
            print("Networks not detected.")
            return False
        
    obj = RSSI_Scan('wlan0') # Object for scanning Wi-Fi networks.
    aps = obj.getRawNetworkScan(True)['output'] # Raw scan data.
    aps = formatCells(str(aps)) # Formatted scan data.
    
    aps = sorted(aps, key=lambda k: k["signal"]) # Sort networks by signal strength.
    closest_ap_location = {} # Dictionary to hold the location of the closest access point.

    # Loop through sorted access points and find the first one with a known location.
    for i in aps:
        if i["mac"] in data:
            closest_ap_location = data[i["mac"]]
            break

    return closest_ap_location # Return the location of the closest access point.


print(get_closest_ap()) # Print details of the closest Wi-Fi access point.
