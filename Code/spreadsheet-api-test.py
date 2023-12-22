import time
import os.path
import datetime
import json

import google.auth  # Google Authentication Library
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build  # Google API Client Library
from googleapiclient.errors import HttpError

## @package google_sheets_updater
#  This script is used for appending and retrieving data from a Google Sheet using the Google Sheets API.

## The ID of the Google Spreadsheet you wish to interact with.
#  Replace this with your actual Sheet ID.
SAMPLE_SPREADSHEET_ID = 'your_spreadsheet_id'

## The range of cells in the sheet to interact with.
#  Adjust as necessary for your specific sheet.
SAMPLE_RANGE_NAME = 'Sheet1!A:G'

## Scopes define the level of access required for the Google Sheets API.
#  Modify these as necessary.
scope = ['https://www.googleapis.com/auth/spreadsheets']

## Attempts to load existing credentials, or generate new ones if necessary.
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', scope)

## Authenticates the user and refreshes credentials if necessary.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scope)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

## @brief Appends values to a specified range within a Google Sheet.
#  @param spreadsheet_id The ID of the spreadsheet to update.
#  @param range_name The A1 notation of the range to update.
#  @param value_input_option How the input data should be interpreted by the API.
#  @param _values The data values to append to the sheet.
#  @param creds The authenticated Google credentials.
#  @return The result of the append operation or an error.
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

## @brief Main execution block.
#  Initializes the Sheets API client, prepares data to append, sends the request,
#  and processes the response. Fetches and prints updated data for verification.
try:
    service = build('sheets', 'v4', credentials=creds)

    # Data to append. Replace with your actual data structure.
    values = [[str(datetime.datetime.now()), "Sample_building", '1', '101', 1000, 100, 23]]
    
    # Append the data to the sheet.
    append_values(SAMPLE_SPREADSHEET_ID, 'Sheet1', 'USER_ENTERED', values, creds)

    # Fetch and print the updated data from the sheet for verification.
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            print('%s, %s' % (row[0], row[4]))

except HttpError as err:
    print(err)
