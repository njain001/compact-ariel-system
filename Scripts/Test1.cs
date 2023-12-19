
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using UnityEngine.Networking;
using System.Collections.Generic;

public class DataUpdaterGoogleSheets1 : MonoBehaviour
{
    //Creating variables for the data to be stored in
    public string spreadsheetId = "1mSJc6b7Vw9tY7NAzHxliYSOvxOwINUsvCGO_Sz5AkMc";
    public string apiKey = "AIzaSyAq_zfMEt71othu0xC092qkkE26AXHxK5w";
    public string sheetName = "Sheet1!A1:H";
    public TMP_InputField inputField;

// This method is generally used to start the process of retreiving the the data from the google sheets  
    void Start()
    {
        // Fetch data initially and set up repeated updates
        StartCoroutine(GetData());
        InvokeRepeating("UpdateData", 5f, 5f);
    }

 // Method to update data by fetching it from Google Sheets
    void UpdateData()
    {
        StartCoroutine(GetData());
    }

// Serializable class to represent the structure of the Google Sheets API response
    [System.Serializable]
    public class SheetsApiResponse
    {
        public string range;
        public string majorDimension;
        public string[][] values;

// Method to create an instance of SheetsApiResponse from JSON
        public static SheetsApiResponse FromJson(string json)
        {
            SheetsApiResponse sheetsApiResponse = new SheetsApiResponse();
            JsonUtility.FromJsonOverwrite(json, sheetsApiResponse);
            return sheetsApiResponse;
        }
    }

// Method to get the last row from a 2D array of values
    object[] GetLastRowFromValues(string[][] values)
    {
        int rowCount = values.GetLength(0);
        int colCount = values.GetLength(1);

        if (rowCount > 0)
        {
            // Create an array to store the values of the last row
            object[] lastRow = new object[colCount];

            // Copy the values from the last row
            for (int col = 0; col < colCount; col++)
            {
                lastRow[col] = values[rowCount - 1][col];
            }

            return lastRow;
        }

        return null; // Return null if there are no rows
    }

 // Coroutine to fetch data from Google Sheets
    IEnumerator GetData()
    {
        Debug.Log("Fetching data from Google Sheets...");

        // Construct the URL for the Google Sheets API request
        string url = $"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheetName}?alt=json&key={apiKey}";

         // Send a UnityWebRequest to the URL
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            yield return www.SendWebRequest();
            // Check if the request was successful
            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"Failed to fetch data. Error: {www.error}");
            }
            else
            {
                //Extract and print the json response
                string jsonResult = www.downloadHandler.text;
                Debug.Log("Google Sheets data fetched successfully.");
                Debug.Log($"JSON Result: {www.downloadHandler.text}");

                string[] substrings = jsonResult.Split("\"values\":")[1].Split("[");
                substrings = substrings[substrings.Length - 1].Split("]");
                Debug.Log($"Type of object:{substrings[0].GetType()}");
                string valuesRow = substrings[0];
                Debug.Log($"The values of the string arr:{valuesRow}");
                Debug.Log($"The datatype of the valuesRow:{valuesRow.GetType()}");
                string[] valuesArray = valuesRow.Split(',');

                // Remove extra characters and quotes from the values
                for (int i = 0; i < valuesArray.Length; i++)
                {
                    valuesArray[i] = valuesArray[i].Replace("\"", "").Trim();
                }

                // Define keys for the data fields
                string[] keys = {
                    "timestamp",
                    "building_name",
                    "floor",
                    "room_no",
                    "co2",
                    "temperature",
                    "humidity",
                    "occupancy"
                };
                 // Create a dictionary to store key-value pairs of data
                Dictionary<string, string> dataMap = new Dictionary<string, string>();

                // Populate the dictionary with data
                for (int i = 0; i < keys.Length && i < valuesArray.Length; i++)
                {
                    dataMap[keys[i]] = valuesArray[i];
                }

                // Print each result with the formatted units
                string logMessage = "DataMap Contents:\n";
                foreach (var entry in dataMap)
                {
                    string formattedValue = FormatValueWithUnit(entry.Key, entry.Value);
                    Debug.Log($"{entry.Key}: {formattedValue}");
                    logMessage += $"{entry.Key}: {formattedValue}\n";
                }
                
                // Method to format values with units based on the data key
                string FormatValueWithUnit(string key, string value)
                {
                    switch (key)
                    {
                        case "co2":
                            return $"{value}ppm";
                        case "temperature":
                            return $"{value}°C";
                        case "humidity":
                            return $"{value}%";
                        default:
                            return value;
                    }
                }
                Debug.Log($"These are the key value pairs : {logMessage}");
                //inputField.text = logMessage; // Set the text of the InputField
                if (inputField != null)
                {
                    inputField.text = logMessage; // Set the text of the InputField
                }
                else
                {
                    Debug.LogError("InputField is not assigned.");
                }
                Debug.Log($"These are the key value pair:{logMessage}");
            }
        }
    }
}
