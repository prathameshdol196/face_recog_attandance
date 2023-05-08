

import os
import csv
import cv2
import face_recognition
import time
import numpy as np



# Load images and learn how to recognize them
known_face_encodings = []
known_face_names = []

for filename in os.listdir("students"):  # list all files in dir
    if filename.endswith('.jpg'):  # if file ends with .jpg
        image_path = os.path.join("students", filename)  # join the path
        image = face_recognition.load_image_file(image_path)  # load image file
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        with open("2023.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ID'] == os.path.splitext(filename)[0]:
                    known_face_names.append(row['Name'])

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Start capturing video from the webcam
video_capture = cv2.VideoCapture(0)

present_students = []  # list of present students
start_time = time.time()
while time.time() - start_time < 600:  # 600 seconds = 10 minutes:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.125, fy=0.125)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, use the name corresponding to the first match.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                if name not in present_students:
                    present_students.append(name)


            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


