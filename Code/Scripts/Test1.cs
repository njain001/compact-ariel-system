using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using UnityEngine.Networking;
using System.Collections.Generic;

/**
 * @file DataUpdaterGoogleSheets1.cs
 * @brief Fetches and updates data from a Google Sheets document.
 *
 * This script fetches data from a specified Google Sheets document using the Google Sheets API
 * and updates the text of a specified TMP_InputField in the Unity scene with this data.
 */

public class DataUpdaterGoogleSheets1 : MonoBehaviour
{
    public string spreadsheetId = "your_spreadsheet_id"; // Replace with your actual spreadsheet ID.
    public string apiKey = "your_api_key"; // Replace with your actual API key.
    public string sheetName = "Sheet1!A1:H"; // The name and range of the sheet to access.
    public TMP_InputField inputField; // Reference to the TMP_InputField where the data will be displayed.

    /**
     * @brief Called before the first frame update.
     *
     * Starts the initial data fetch and sets up a repeating call to update the data every 5 seconds.
     */
    void Start()
    {
        StartCoroutine(GetData()); // Fetch data initially.
        InvokeRepeating("UpdateData", 5f, 5f); // Set up repeated updates every 5 seconds.
    }

    /**
     * @brief Initiates fetching of data from Google Sheets.
     *
     * Called at a regular interval to keep the displayed data up-to-date.
     */
    void UpdateData()
    {
        StartCoroutine(GetData());
    }

    /**
     * @brief Serializable class to represent the structure of the Google Sheets API response.
     */
    [System.Serializable]
    public class SheetsApiResponse
    {
        public string range; // The cell range fetched.
        public string majorDimension; // The major dimension of the data (ROWS or COLUMNS).
        public string[][] values; // The values fetched from the sheet.

        /**
         * @brief Creates an instance of SheetsApiResponse from JSON.
         * @param json The JSON string to parse.
         * @return An instance of SheetsApiResponse.
         */
        public static SheetsApiResponse FromJson(string json)
        {
            SheetsApiResponse sheetsApiResponse = new SheetsApiResponse();
            JsonUtility.FromJsonOverwrite(json, sheetsApiResponse);
            return sheetsApiResponse;
        }
    }

    /**
     * @brief Coroutine to fetch data from Google Sheets.
     *
     * Constructs a URL for the Google Sheets API request, sends the request,
     * and processes the response to extract and display the data.
     */
    IEnumerator GetData()
    {
        Debug.Log("Fetching data from Google Sheets...");

        string url = $"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheetName}?alt=json&key={apiKey}";

        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"Failed to fetch data. Error: {www.error}");
            }
            else
            {
                // Extract and print the json response
                string jsonResult = www.downloadHandler.text;
                Debug.Log("Google Sheets data fetched successfully.");
                Debug.Log($"JSON Result: {www.downloadHandler.text}");

                // Parse the JSON response
                SheetsApiResponse response = SheetsApiResponse.FromJson(jsonResult);

                // If there are values, get the last row and update the input field
                if (response.values != null && response.values.Length > 0)
                {
                    string[] lastRow = response.values[response.values.Length - 1];
                    string displayText = string.Join(", ", lastRow); // Combine the row's values for display
                    if (inputField != null)
                    {
                        inputField.text = displayText; // Set the text of the InputField
                    }
                    else
                    {
                        Debug.LogError("InputField is not assigned.");
                    }
                }
                else
                {
                    Debug.Log("No data found in the specified range.");
                }
            }
        }
    }
}
