
import os
import csv
import cv2
import face_recognition
import time
import numpy as np
import datetime
import pandas as pd
from tkinter import *
from tkinter import messagebox
import random


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


def start_attendance():
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


def login():
    username = username_entry.get()
    password = password_entry.get()
    college = college_entry.get()


    # Check if the login credentials are valid
    with open(file="teachers/data.json") as file:
        pass

    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
        open_main_window()

    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def open_main_window():
    login_window.destroy()

    # Create the main window
    main_window = Tk()
    main_window.title("Attendance System")
    main_window.geometry("400x200")

    # GUI components and functionalities for the main window
    start_button = Button(main_window, text="Start Attendance", command=start_attendance)
    start_button.grid(column=1, row=1)

    main_window.mainloop()


def open_signup_window():
    login_window.destroy()

    def signup():
        email = signup_email_entry.get()
        password = signup_email_entry.get()
        name = name_entry.get()
        college = college_entry.get()


    # Create the signup window
    signup_window = Tk()
    signup_window.title("Sign Up")
    signup_window.geometry("400x200")
    signup_window.config(padx=50, pady=50, bg="#313552", )

    # GUI components and functionalities for the signup window

    # Username label and entry
    signup_email_label = Label(signup_window, text="Username: ", bg="#313552")
    signup_email_label.grid(column=1, row=1)
    signup_email_entry = Entry(signup_window, width=42)
    signup_email_entry.grid(column=2, row=1, columnspan=2)

    # Password label and entry
    password_label = Label(signup_window, text="Email: ", bg="#313552")
    password_label.grid(column=1, row=2)
    signup_password_entry = Entry(signup_window, width=42)
    signup_password_entry.grid(column=2, row=2, columnspan=2)

    # College label and entry
    college_label = Label(signup_window, text="College: ", bg="#313552")
    college_label.grid(column=1, row=3)
    college_entry = Entry(signup_window, width=42)
    college_entry.grid(column=2, row=3, columnspan=2)

    # Name label and entry
    name_label = Label(signup_window, text="Name: ", bg="#313552")
    name_label.grid(column=1, row=4)
    name_entry = Entry(signup_window, width=42)
    name_entry.grid(column=2, row=4, columnspan=2)

    # Signup button
    signup_button = Button(signup_window, text="Sign Up", command=signup)
    signup_button.grid(column=2, row=5)


login_window = Tk()
login_window.title("Login")
login_window.geometry("400x200")
login_window.config(padx=50, pady=50, bg="#313552",)

# Username label and entry
username_label = Label(login_window, text="Username: ", bg="#313552")
username_label.grid(column=1, row=1)
username_entry = Entry(login_window, width=42)
username_entry.grid(column=2, row=1, columnspan=2)

# Password label and entry
password_label = Label(login_window, text="Password: ", bg="#313552")
password_label.grid(column=1, row=2)
password_entry = Entry(login_window, show="*", width=42)
password_entry.grid(column=2, row=2, columnspan=2)

# Password label and entry
college_label = Label(login_window, text="College: ", bg="#313552")
college_label.grid(column=1, row=3)
college_entry = Entry(login_window, width=42)
college_entry.grid(column=2, row=3, columnspan=2)

# Login button
login_button = Button(login_window, text="Login", command=login)
login_button.grid(column=3, row=4)

# Signup button
signup_button = Button(login_window, text="Sign Up", command=open_signup_window)
signup_button.grid(column=2, row=4)

login_window.mainloop()


