import cv2 as cv
import numpy as np
import time
import Person
import matplotlib.pyplot as plt
import busio
import board
import os
import datetime

# Read sensor data
def read_thermal_sensor_data(sensor):
    frame = [0] * 768
    try:
        sensor.getFrame(frame)
    except ValueError:
        # In case of read error, retry
        sensor.getFrame(frame)
    return frame


# Process IR Data (This part will need significant adaptation)
def process_ir_data(frame):
    # Example: Reshape and normalize the IR data
    ir_array = np.array(frame).reshape(24, 32)
    normalized_ir = cv.normalize(ir_array, None, 0, 255, cv.NORM_MINMAX)
    converted_ir = np.uint8(normalized_ir)
    return converted_ir

# Function to detect persons from the thermal image
def detect_and_track_persons(frame, cnt_up=0, cnt_down=0):
    h = 24
    w = 32
    frameArea = h * w
    areaTH = frameArea / 250

    # Entry/exit lines
    line_up = int(2 * (h / 5))
    line_down = int(3 * (h / 5))
        
    # Thresholding to find hot spots (potential people)
    _, thresh = cv.threshold(frame, 200, 255, cv.THRESH_BINARY)

    # Find contours
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        M = cv.moments(contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # Check if the contour (person) crosses the line
            if cy < line_up:
                cnt_up += 1
            elif cy > line_down:
                cnt_down += 1

            # Draw the contour and center for visualization
            cv.drawContours(frame, [contour], -1, (0, 255, 0), 3)
            cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    return frame, cnt_up, cnt_down

# In case the user wants the image captured by the sensor, this will output the thermal image
def visualize_data(frame, index):
    plt.imshow(frame, cmap='hot', interpolation='nearest')
    
    # Create a directory for saving images if it doesn't exist
    os.makedirs('thermal_images', exist_ok=True)

    # Save the figure to a file
    plt.savefig(f'thermal_images/thermal_image_{index}.png')

    # Clear the current figure to free memory and avoid overlap
    plt.clf()


# Function to get the occupant count. This is the client-side function which is used in other methods/files
def get_occupancy_count(sensor, save_image=False):    
    # Read data from IR sensor
    ir_data = read_thermal_sensor_data(sensor)
    processed_frame = process_ir_data(ir_data)

    processed_frame, cnt_up, cnt_down = detect_and_track_persons(processed_frame)
    
    if save_image:
        visualize_data(processed_frame, datetime.datetime.now())
        
    total_people = abs(cnt_up - cnt_down)
    return total_people
