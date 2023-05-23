

from tkinter import *
from tkinter import messagebox


def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the login credentials are valid
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
    main_window.geometry("200x200")

    # Add your GUI components and functionalities for the main window here
    start_button = Button(main_window, text="Start Attendance", command=start_attendance)

    main_window.mainloop()


def open_signup_window():
    signup_window = Toplevel(login_window)
    signup_window.title("Sign Up")
    signup_window.geometry("200x200")

    # Add your GUI components and functionalities for the signup window here


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

# Login button
login_button = Button(login_window, text="Login", command=login)
login_button.grid(column=3, row=3)

# Signup button
signup_button = Button(login_window, text="Sign Up", command=open_signup_window)
signup_button.grid(column=2, row=3)

login_window.mainloop()
