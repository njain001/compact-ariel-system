import time
import board
import adafruit_scd4x
import busio
import os.path
import datetime
import json
import smbus2
import adafruit_mlx90640
from gpiozero import DigitalInputDevice, DigitalOutputDevice


import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from geolocation_data import get_closest_ap
from occupancy import get_occupancy_count

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = 'your_sheet_id' 
SAMPLE_RANGE_NAME = 'Sheet1!A:H' # Add following columns in the sheet {timestamp, building_name, floor, room_no, co2, temperature, humidity, occupancy_count]

# If modifying these scopes, delete the file token.json.
scope = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticating using the token.json. In case there's no token.json available, it will create new using credentials.json file.
creds = None
if os.path.exists('token.json'):
  creds = Credentials.from_authorized_user_file('token.json', scope)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', scope)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


# Appends the final data row in the google sheets
def append_values(spreadsheet_id, range_name, value_input_option, _values, creds):
    try:
        service = build('sheets', 'v4', credentials=creds)

        body = {
            'values': _values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        
        print("Data appended")

        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


# Initialized thermal sensor with default configuration
def initialize_thermal_sensor(i2c):
    sensor = adafruit_mlx90640.MLX90640(i2c)
    sensor.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ  # set refresh rate
    return sensor

# Main code block, this calls all the necessary functions to fetch the data for sensors
try:
    service = build('sheets', 'v4', credentials=creds)
    
    
    i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
    other_i2c = busio.I2C(board.SCL, board.SDA)
    scd4x = adafruit_scd4x.SCD4X(i2c)
    
    thermal_sensor = initialize_thermal_sensor(i2c)    
    
    ap_dict = get_closest_ap()
    building, floor, room = ap_dict['building'], ap_dict['floor'], ap_dict['room']
    
    while True:
        try:
            occupant = get_occupancy_count(thermal_sensor, save_image=True)
            
            scd4x.measure_single_shot()
            values = [[str(datetime.datetime.now()), building, floor, room, scd4x.CO2, scd4x.temperature, scd4x.relative_humidity, occupant]]
            append_values(SAMPLE_SPREADSHEET_ID, 'Sheet1', 'USER_ENTERED', values, creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(5.0)
            continue
            

        time.sleep(5.0)
except HttpError as err:
    print(err)


