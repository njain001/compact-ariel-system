## @package thermal_tracking
#  This module contains functions for reading and processing data from a thermal sensor,
#  detecting and tracking persons in a thermal image, and visualizing the data.

import cv2 as cv  ## OpenCV library for image processing.
import numpy as np  ## NumPy library for numerical operations.
import time  ## Time module for time-related functions.
import Person  ## Custom module for handling person-related data.
import matplotlib.pyplot as plt  ## Matplotlib for creating visualizations.
import busio  ## BusIO library for interacting with I2C/SPI/UART.
import board  ## Board library for accessing hardware pins.
import os  ## OS module for interacting with the operating system.
import datetime  ## Datetime module for handling date and time.

## Function to read data from a thermal sensor.
#  @param sensor The thermal sensor object from which to read.
#  @return A list of temperature readings representing the captured frame data.
def read_thermal_sensor_data(sensor):
    frame = [0] * 768  # Initialize frame array for sensor data (assuming 768 data points)
    try:
        sensor.getFrame(frame)  # Attempt to read data from the sensor
    except ValueError:
        # In case of a read error, retry once
        sensor.getFrame(frame)
    return frame  # Return the captured frame data

## Function to process infrared (IR) data.
#  @param frame A list of temperature readings from the thermal sensor.
#  @return A 24x32 numpy array of 8-bit values representing the processed IR data.
def process_ir_data(frame):
    # Reshape the IR data into a 24x32 array (assumed sensor resolution)
    ir_array = np.array(frame).reshape(24, 32)
    # Normalize the IR data for uniform intensity distribution
    normalized_ir = cv.normalize(ir_array, None, 0, 255, cv.NORM_MINMAX)
    # Convert normalized data to 8-bit for image processing
    converted_ir = np.uint8(normalized_ir)
    return converted_ir

## Function to detect and track persons in a thermal image.
#  @param frame The processed thermal image data.
#  @param cnt_up (Optional) Initial count of people moving up.
#  @param cnt_down (Optional) Initial count of people moving down.
#  @return A tuple containing the processed frame and updated counts.
def detect_and_track_persons(frame, cnt_up=0, cnt_down=0):
    # Define frame dimensions and threshold area for detection
    h, w = 24, 32
    frameArea = h * w
    areaTH = frameArea / 250

    # Define lines for counting entry and exit
    line_up = int(2 * (h / 5))
    line_down = int(3 * (h / 5))
        
    # Apply binary thresholding to find hot spots (potential persons)
    _, thresh = cv.threshold(frame, 200, 255, cv.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Process each detected contour
    for contour in contours:
        M = cv.moments(contour)  # Calculate moments for contour
        if M['m00'] != 0:  # Check for division by zero
            # Compute centroid of the contour
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # Count crossings over the predefined lines
            if cy < line_up:
                cnt_up += 1
            elif cy > line_down:
                cnt_down += 1

            # Visualize the contour and its centroid
            cv.drawContours(frame, [contour], -1, (0, 255, 0), 3)
            cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    return frame, cnt_up, cnt_down  # Return processed frame and counts

## Function to visualize and save the thermal data as an image.
#  @param frame The processed frame to visualize.
#  @param index An identifier for the image, typically a timestamp.
#  Creates and saves a heatmap representation of the thermal data.
def visualize_data(frame, index):
    plt.imshow(frame, cmap='hot', interpolation='nearest')
    
    # Create a directory for saving images, if it doesn't exist
    os.makedirs('thermal_images', exist_ok=True)

    # Save the image with a timestamp in the filename
    plt.savefig(f'thermal_images/thermal_image_{index}.png')

    # Clear the figure to free memory and avoid overlap
    plt.clf()

## Main function to get the occupancy count.
#  @param sensor The thermal sensor object to use for data acquisition.
#  @param save_image (Optional) A boolean indicating whether to save the processed frame as an image.
#  @return The total number of people detected.
def get_occupancy_count(sensor, save_image=False):    
    # Read and process data from the IR sensor
    ir_data = read_thermal_sensor_data(sensor)
    processed_frame = process_ir_data(ir_data)

    # Detect and track persons in the processed frame
    processed_frame, cnt_up, cnt_down = detect_and_track_persons(processed_frame)
    
    # Optionally visualize and save the processed frame
    if save_image:
        visualize_data(processed_frame, datetime.datetime.now())
        
    # Calculate the total number of people (assuming entry-exit model)
    total_people = abs(cnt_up - cnt_down)
    return total_people
