from config import * #type: ignore
from tkinter import *

class ProfilePage(object):
    def __init__(self, parent_frame):
        self.frame = Frame(master=parent_frame, bg=BACKGROUND) #type: ignore
        self.frame.pack(fill="both", expand=True, padx=30, pady=15)

        title_label = Label(master=self.frame, text="Profile", bg=BACKGROUND, fg=BLACK, font=TITLE) #type: ignore
        name_label = Label(master=self.frame, text="Name:", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore
        email_label = Label(master=self.frame, text="Email: ", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore

        self.name_entry = Entry(master=self.frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.email_entry = Entry(master=self.frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore

        update_btn = Button(master=self.frame, text="Update Profile", bg=WHITE, fg=BLACK, font=LABEL_12, command=self.update_profile) #type: ignore

        sub_title_label = Label(master=self.frame, text="Change Password", bg=BACKGROUND, fg=BLACK, font=LABEL_16) #type: ignore
        current_pwd = Label(master=self.frame, text="Current", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore
        password = Label(master=self.frame, text="New", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore
        cpassword = Label(master=self.frame, text="Confirm", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore

        self.current_entry = Entry(master=self.frame, show="*", bg=WHITE, fg=BLACK, font=LABEL_12) #type: ignore
        self.password_entry = Entry(master=self.frame, show="*", bg=WHITE, fg=BLACK, font=LABEL_12) #type: ignore
        self.cpassword_entry = Entry(master=self.frame, show="*", bg=WHITE, fg=BLACK, font=LABEL_12) #type: ignore

        change_pwd_btn = Button(master=self.frame, text="Update Profile", bg=WHITE, fg=BLACK, font=LABEL_12, command=self.change_pwd) #type: ignore

        title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="w")

        name_label.grid(row=1, column=0, sticky="w")
        self.name_entry.grid(row=1, column=1, pady=10)

        email_label.grid(row=2, column=0,  sticky="w")
        self.email_entry.grid(row=2, column=1, pady=10)

        update_btn.grid(row=3, column=1)

        sub_title_label.grid(row=4, column=0, columnspan=2, pady=20,  sticky="w")

        current_pwd.grid(row=5, column=0,  sticky="w")
        self.current_entry.grid(row=5, column=1, pady=10)

        password.grid(row=6, column=0,  sticky="w")
        self.password_entry.grid(row=6, column=1, pady=10)

        cpassword.grid(row=7, column=0,  sticky="w")
        self.cpassword_entry.grid(row=7, column=1, pady=10)

        change_pwd_btn.grid(row=8, column=1)



    def update_profile(self):
        print("update profile")


    def change_pwd(self):
        print("change password")