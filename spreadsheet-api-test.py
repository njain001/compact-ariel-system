import time
import os.path
import datetime
import json

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# import smbus

# # Define the I2C address of the SCD30 sensor
# SCD30_I2C_ADDRESS = 0x61

# # Initialize I2C bus
# i2c = smbus.SMBus(1)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1mSJc6b7Vw9tY7NAzHxliYSOvxOwINUsvCGO_Sz5AkMc'
SAMPLE_RANGE_NAME = 'Sheet1!A:G'

# If modifying these scopes, delete the file token.json.
scope = ['https://www.googleapis.com/auth/spreadsheets']

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

        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

try:
    service = build('sheets', 'v4', credentials=creds)

    values = [[str(datetime.datetime.now()), "Sample_building", '1', '101', 1000, 100, 23]]
    
    append_values(SAMPLE_SPREADSHEET_ID, 'Sheet1', 'USER_ENTERED', values, creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    print('Name, Major:')
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        print('%s, %s' % (row[0], row[4]))
except HttpError as err:
    print(err)


