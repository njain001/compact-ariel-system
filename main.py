import cv2
import numpy as np
import tensorflow as tf

# Load the saved model
model_path = ("/home/karan/Karan/Umass Boston/3. Fall 2023/cs682 - Software Development Laboratory/Tensorflow "
              "Model/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model")
model = tf.saved_model.load(model_path)

# Load the image
image = cv2.imread("image.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (300, 300))
image = image / 255.0  # Normalize image to the range [0, 1] as float32

# Convert the image to tf.uint8 data type
input_tensor = tf.convert_to_tensor(image * 255, dtype=tf.uint8)[tf.newaxis, ...]

# Perform inference
detections = model(input_tensor)

person_count = 0

# Assume class label for "person" is 1 (may vary depending on the model)
person_class = 1

# Access detection boxes, classes, and scores
detection_boxes = detections['detection_boxes'][0].numpy()
detection_classes = detections['detection_classes'][0].numpy()
detection_scores = detections['detection_scores'][0].numpy()

for i in range(len(detection_classes)):
    if detection_classes[i] == person_class and detection_scores[i] > 0.5:
        person_count += 1

print(f"Number of people in the image: {person_count}")
