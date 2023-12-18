# compact-ariel-system
Create 3D model of building integrating room data such as temperature, humidity etc

## Sensor Data Acquisition
Captures the sensor data (co2, humidity, temperature and occupancy count) and store them to the google sheets.

### Setup
- Attach the SCD40 and MLX90640 sensors to the Raspberry Pi hub. Use the pin #3 & #5 for data and clock respectively.
- Please add the code from sensor folder to the raspberry pi hub and setup the code.

### Token Generation
- Please visit GCC (https://console.cloud.google.com/).
- Login or create user on Google Cloud Console (GCC).
- Enable Google Sheets API service.
- Complete the process and create a credentials.json file.
- Move credentials.json file with the other code
- When running the code, you need to complete the authentication flow. This will generate the token.json file

Visit this site for detailed step by step process: https://developers.google.com/sheets/api/quickstart/python

### Google Sheets
We will use google sheets to capture the data. Follow below steps to configure google sheets with the code.
- Create a Google sheets with the same email that was used for token generation.
- DO NOT RENAME the sheet name and keep it default i.e. "Sheet1"
- Added following columns in the mentioned order: [timestamp, building_name, floor, room_no, co2, temperature, humidity, occupancy_count]
- Update the google sheet ID in the store_sensor_data.py file wih your sheet ID.

### Installation
- Install requirements from the requirements.txt
```bash
  pip3 install -r requirements.txt
```

### Data Capturing
- Run the script using following command
```bash
  python3 store_sensor_data.py
```
Once you follow the steps above, you'll find sensor data being captured in your Google Sheets.
