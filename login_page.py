from config import *
from tkinter import *
from tkinter import messagebox as mb

class LoginPage(object):
    def __init__(self, parent_window):
        self.login_frame = Frame(master=parent_window, bg=BACKGROUND) # type: ignore
        #labels
        login_label = Label(master=self.login_frame, text="Login", bg=BACKGROUND, fg=BLACK, font=TITLE) # type: ignore
        email_label = Label(master=self.login_frame, text="Email", bg=BACKGROUND, fg=BLACK, font=LABEL_14) # type: ignore
        password_label = Label(master=self.login_frame, text="Password:", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore

        #entries
        self.email_entry = Entry(master=self.login_frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.password_entry = Entry(master=self.login_frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore

        #buttons
        login_btn = Button(master=self.login_frame, text="Login", bg=WHITE, font=LABEL_14, command=self.login) #type: ignore
        register_btn = Button(master=self.login_frame, text="Register", bg=WHITE, font=LABEL_12) #type: ignore

        #placing the frames and items
        self.login_frame.pack()

        login_label.grid(column=0, row=0, columnspan=2, pady=30)

        email_label.grid(column=0, row=1)
        self.email_entry.grid(column=1, row=1, pady=10)

        password_label.grid(column=0, row=2)
        self.password_entry.grid(column=1, row=2, pady=10)

        login_btn.grid(column=0, row=3, columnspan=2, pady=20)
        register_btn.grid(column=0, row=4, columnspan=2)

        self.email_entry.focus()

    def login(self):
        print("Test login")

class RegisterPage(object):
    def __init__(self, parent_window):
        self.register_frame = Frame(master=parent_window, bg=BACKGROUND) # type: ignore
        #labels
        register_label = Label(master=self.register_frame, text="Register", bg=BACKGROUND, fg=BLACK, font=TITLE) # type: ignore
        name_label = Label(master=self.register_frame, text="Name", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore
        email_label = Label(master=self.register_frame, text="Email", bg=BACKGROUND, fg=BLACK, font=LABEL_14) # type: ignore
        password_label = Label(master=self.register_frame, text="Password:", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore
        cpassword_label = Label(master=self.register_frame, text="Confirm:", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore

        #entries
        self.name_entry = Entry(master=self.register_frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.email_entry = Entry(master=self.register_frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.password_entry = Entry(master=self.register_frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.cpassword_entry = Entry(master=self.register_frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore

        #buttons
        register_btn = Button(master=self.register_frame, text="Register", bg=WHITE, font=LABEL_14, command=self.register) #type: ignore
        login_btn = Button(master=self.register_frame, text="Login", bg=WHITE, font=LABEL_12) #type: ignore

        self.register_frame.pack()

        #placing the items inside the register frame
        register_label.grid(row=0, column=0, columnspan=2, pady=30)

        name_label.grid(row=1, column=0)
        self.name_entry.grid(row=1, column=1, pady=10)

        email_label.grid(row=2, column=0)
        self.email_entry.grid(row=2, column=1, pady=10)

        password_label.grid(row=3, column=0)
        self.password_entry.grid(row=3, column=1, pady=10)

        cpassword_label.grid(row=4, column=0)
        self.cpassword_entry.grid(row=4, column=1, pady=10)

        register_btn.grid(row=5, column=0, columnspan=2,  pady=10)
        login_btn.grid(row=6, column=0, columnspan=2)


    def register(self):
        print("Register")