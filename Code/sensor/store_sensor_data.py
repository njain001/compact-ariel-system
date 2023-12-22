import time  ## Module for time-related tasks.
import board  ## Provides access to the physical board's pins.
import adafruit_scd4x  ## Library for the SCD4x CO2 sensor.
import busio  ## Library for handling I2C and SPI communications.
import os.path  ## Module for common pathname manipulations.
import datetime  ## Module for manipulating dates and times.
import json  ## Module for JSON encoding and decoding.
import smbus2  ## SMBus2 module for I2C communications.
import adafruit_mlx90640  ## Library for the MLX90640 thermal camera.
from gpiozero import DigitalInputDevice, DigitalOutputDevice  ## Library for interfacing with GPIO pins.

# Google API and authentication libraries.
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Custom modules for geolocation and occupancy detection.
from geolocation_data import get_closest_ap
from occupancy import get_occupancy_count

## @package environmental_monitoring
#  This script interfaces with various sensors and the Google Sheets API to read sensor data,
#  process it, and then append it to a spreadsheet.

# Constants for Google Sheets API.
SAMPLE_SPREADSHEET_ID = 'your_sheet_id'  ## Replace with your actual Sheet ID.
SAMPLE_RANGE_NAME = 'Sheet1!A:H'  ## The range of cells to interact with in the sheet.

# Scopes define the level of access required. Modify as needed.
scope = ['https://www.googleapis.com/auth/spreadsheets']

## Authenticates the user with Google Sheets API using OAuth 2.0.
#  It checks for existing credentials or creates new ones if necessary.
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', scope)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', scope)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

## Appends the final data row in the Google Sheets.
#  @param spreadsheet_id The ID of the spreadsheet.
#  @param range_name The range of cells to interact with.
#  @param value_input_option Specifies how the input data should be interpreted.
#  @param _values The data values to append.
#  @param creds The authenticated credentials.
#  @return The result of the append operation or an error.
def append_values(spreadsheet_id, range_name, value_input_option, _values, creds):
    try:
        service = build('sheets', 'v4', credentials=creds)
        body = {'values': _values}
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            insertDataOption="INSERT_ROWS",
            body=body).execute()
        print("Data appended")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

## Initializes the MLX90640 thermal sensor with default configuration.
#  @param i2c The I2C bus used to communicate with the sensor.
#  @return The initialized sensor object.
def initialize_thermal_sensor(i2c):
    sensor = adafruit_mlx90640.MLX90640(i2c)
    sensor.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ  # Set refresh rate
    return sensor

## Main code block. This calls all necessary functions to fetch and append data to Google Sheets.
try:
    service = build('sheets', 'v4', credentials=creds)
    
    i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)  # Fast I2C connection for thermal sensor.
    other_i2c = busio.I2C(board.SCL, board.SDA)  # Standard I2C connection.
    scd4x = adafruit_scd4x.SCD4X(i2c)  # Initialize the CO2 sensor.
    
    thermal_sensor = initialize_thermal_sensor(i2c)  # Initialize thermal sensor.
    
    ap_dict = get_closest_ap()  # Fetch the closest access point's data.
    building, floor, room = ap_dict['building'], ap_dict['floor'], ap_dict['room']  # Extract location details.
    
    while True:  # Main loop to continuously fetch data and update the sheet.
        try:
            occupant = get_occupancy_count(thermal_sensor, save_image=True)  # Get the occupancy count.
            
            scd4x.measure_single_shot()  # Take a single measurement of CO2, temp, and humidity.
            values = [[str(datetime.datetime.now()), building, floor, room, scd4x.CO2, scd4x.temperature, scd4x.relative_humidity, occupant]]
            append_values(SAMPLE_SPREADSHEET_ID, 'Sheet1', 'USER_ENTERED', values, creds)  # Append the data to the sheet.

            # Call the Sheets API to read back the data for verification (optional).
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')

        except RuntimeError as error:  # Handle specific errors from the sensors.
            print(error.args[0])
            time.sleep(5.0)  # Wait for a while before retrying.
            continue

        time.sleep(5.0)  # Delay before the next reading.
except HttpError as err:  # Handle HTTP errors from Google Sheets API.
    print(err)
