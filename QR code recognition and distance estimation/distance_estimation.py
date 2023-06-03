import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model

# Load classification model
# model = load_model('my_model.tflite')
model = tf.lite.Interpreter('my_model.tflite')
model.allocate_tensors()
input_details = model.get_input_details()
output_details = model.get_output_details()

# Load detection model
net = cv2.dnn.readNet('yolov3_testing.cfg', 'yolov3_training_last.weights')

# print(model.summary())

# Set up the camera
cap = cv2.VideoCapture(1)
distances = []
frame_count = 0
max_frames = 10

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
print("Layer names: ", layer_names)
print("Output kayers: ", output_layers)

# camera parameters
qrcode_size_cm = 24  # 9.5
focal_length_mm = 0.99 # 0.99 # 3.04  # 0.99
sensor_width_mm = 6.35# 4.62 # 6.35
pixel_size_mm = 0.00009  # 0.00000112 # 0.109

print("Starting detection loop")
while True:
    ret, frame = cap.read()
    height, width, channels = frame.shape
    if ret:
        frame_count += 1

    if frame_count >= max_frames:
        break

    # Perform object detection
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Loop over detected objects
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Extract ROI from input image
                x, y, w, h = detection[:4] * np.array([frame.shape[1], frame.shape[0],
                                                       frame.shape[1], frame.shape[0]])
                x, y, w, h = int(x - w / 2), int(y - h / 2), int(w), int(h)
                if x < frame.shape[1] and y < frame.shape[0] and x+w < frame.shape[1] and y+h < frame.shape[0]:
                    roi = frame[y : y+h, x : x+w]
                    if roi.size != 0:
                        ROI = cv2.resize(roi, (224, 224))

                    # Perform classification on ROI
                    input_tensor = tf.keras.preprocessing.image.img_to_array(ROI)
                    input_tensor /= 255.
                    input_tensor = np.expand_dims(input_tensor, axis=0)

                    model.set_tensor(input_details[0]['index'], input_tensor)
                    model.invoke()
                    predictions = model.get_tensor(output_details[0]['index'])

                    # predictions = model.predict(input_tensor)
                    predicted_class = np.argmax(predictions)
                    print("Predicted class = ", predicted_class)

                    if predicted_class == 0:
                        object_width_pixels = w
                        # distance_m = (qrcode_size_cm * focal_length_mm) / object_width_pixels
                        # distance_m = (focal_length_mm * qrcode_size_cm * height) / (width * pixel_size_mm * width)
                        distance_m = (qrcode_size_cm * focal_length_mm) / (object_width_pixels * pixel_size_mm)
                        cv2.putText(frame, f"Distance: {distance_m:.2f} m", (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    distances.append(distance_m)
                    print("Distance = ", distance_m)

    # Display frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) == ord('q'):
            break

sum = 0
average_distance = 0
for i in distances:
    sum += i
    average_distance = sum / len(distances)
print(average_distance)

# Release resources
cap.release()
cv2.destroyAllWindows()