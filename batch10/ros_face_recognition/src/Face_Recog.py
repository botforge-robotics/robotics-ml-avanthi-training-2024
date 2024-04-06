import cv2  # For Image processing
import numpy as np  # For converting Images to Numerical array
import os  # To handle directories

labels = ["chaitu", "Elon Musk"]

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=15, neighbors=20, grid_x=10, grid_y=10)
recognizer.read("face-trainner.yml")

cap = cv2.VideoCapture(0)  # Get video feed from the Camera

# Create window to display sliders
cv2.namedWindow('Parameters')

# Create sliders for adjusting parameters
cv2.createTrackbar('Scale Factor', 'Parameters', 15, 50, lambda x: None)
cv2.createTrackbar('Min Neighbors', 'Parameters', 6, 20, lambda x: None)
cv2.createTrackbar('Confidence Threshold', 'Parameters',
                   90, 100, lambda x: None)

while (True):
    ret, img = cap.read()  # Break video into frames
    # Convert Video frame to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Get current slider values
    scaleFactor = cv2.getTrackbarPos('Scale Factor', 'Parameters') / 10.0
    minNeighbors = cv2.getTrackbarPos('Min Neighbors', 'Parameters')
    confThreshold = cv2.getTrackbarPos('Confidence Threshold', 'Parameters')

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        id_, conf = recognizer.predict(roi_gray)
        if conf >= confThreshold:
            font = cv2.FONT_HERSHEY_SIMPLEX  # Font style for the name
            name = labels[id_]  # Get the name from the List using ID number
            cv2.putText(img, name, (x, y), font, 1, (0, 0, 255), 2)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('Preview', img)  # Display the Video
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
