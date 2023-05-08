
import os
import csv
import cv2
import face_recognition
import time
import numpy as np
import datetime
import pandas as pd


def known_student_names():
    print("in known_student_names")
    face_names = []
    for filename in os.listdir("students"):  # list all files in dir
        if filename.endswith('.jpg'):  # if file ends with .jpg
            with open("attendance.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ID'] == os.path.splitext(filename)[0]:
                        face_names.append(row['Name'])
    return face_names


def known_student_face_encodings():
    print("in known_student_face_encodings")
    # Load images and recognize them
    face_encodings = []
    for filename in os.listdir("students"):  # list all files in dir
        if filename.endswith('.jpg'):  # if file ends with .jpg
            image_path = os.path.join("students", filename)  # join the path
            image = face_recognition.load_image_file(image_path)  # load image file
            face_encoding = face_recognition.face_encodings(image)[0]
            face_encodings.append(face_encoding)
    return face_encodings


def attendance(present_list):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv('attendance.csv')

    # Add a new column with today's date, if it doesn't already exist
    today = datetime.date.today().strftime('%Y-%m-%d')
    if today not in df.columns:
        df[today] = ''

    # Iterate through the present_list and mark each student as present
    for student in present_list:
        # Convert student's name to lowercase for comparison
        student_lower = student.lower()

        # Find the row index where the student's name matches in the DataFrame
        student_row_index = df.index[df['Name'].str.lower() == student_lower]

        # If the student is in the DataFrame, mark them as present for today
        if len(student_row_index) > 0:
            row = student_row_index[0]
            if df.at[row, today] != 'present':
                df.at[row, today] = 'present'

    # Write the updated DataFrame back to the CSV file
    df.to_csv('attendance.csv', index=False)


known_face_names = known_student_names()
print("known_face_names")
known_face_encodings = known_student_face_encodings()
print("known_face_encodings")

video_capture = cv2.VideoCapture(0)  # capture video
present_list = []
start_time = time.time()
while time.time() - start_time < 6:  # 600 seconds = 10 minutes:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    faces_in_frame = face_recognition.face_locations(small_frame)  # face locations
    faces_in_frame_encoding = face_recognition.face_encodings(small_frame, faces_in_frame)  # encoding

    for encode, faceloc in zip(faces_in_frame_encoding, faces_in_frame):
        matches = face_recognition.compare_faces(known_face_encodings, encode)
        face_dis = face_recognition.face_distance(known_face_encodings, encode)
        matchIndex = np.argmin(face_dis)
        # name = "unknown"
        print("in for encode, faceloc in zip(faces_in_frame_encoding, faces_in_frame) ")

        if matches[matchIndex]:
            name = known_face_names[matchIndex].title()
            print("attendance")
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            # draw a box around face
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(frame, (x1, y2 - 25), (x2, y2), (0, 0, 255), cv2.FILLED)

            # Draw a label with a name below the face
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            if name not in present_list:
                present_list.append(name)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

attendance(present_list)
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

