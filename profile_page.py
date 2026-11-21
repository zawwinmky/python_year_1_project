from config import * #type: ignore
from tkinter import *
import database as db
from database import ProfileError
from tkinter import messagebox as mb


class ProfilePage(object):
    def __init__(self, parent_frame, user):
        self.user = user

        self.frame = Frame(master=parent_frame, bg=BACKGROUND) #type: ignore
        self.frame.pack(fill="both", expand=True, padx=30, pady=15)

        title_label = Label(master=self.frame, text="Profile", bg=BACKGROUND, fg=BLACK, font=TITLE) #type: ignore
        name_label = Label(master=self.frame, text="Name:", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore
        email_label = Label(master=self.frame, text="Email: ", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore

        self.name_entry = Entry(master=self.frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.email_entry = Entry(master=self.frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.name_entry.insert(0, self.user["name"])
        self.email_entry.insert(0, self.user["email"])

        update_btn = Button(master=self.frame, text="Update Profile", bg=WHITE, fg=BLACK, font=LABEL_12, command=self.update_profile) #type: ignore

        sub_title_label = Label(master=self.frame, text="Change Password", bg=BACKGROUND, fg=BLACK, font=LABEL_14) #type: ignore
        current_pwd = Label(master=self.frame, text="Current", bg=BACKGROUND, fg=BLACK, font=LABEL_12) #type: ignore
        password = Label(master=self.frame, text="New", bg=BACKGROUND, fg=BLACK, font=LABEL_12) #type: ignore
        cpassword = Label(master=self.frame, text="Confirm", bg=BACKGROUND, fg=BLACK, font=LABEL_12) #type: ignore

        self.current_entry = Entry(master=self.frame, show="*", bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.password_entry = Entry(master=self.frame, show="*", bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.cpassword_entry = Entry(master=self.frame, show="*", bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore

        change_pwd_btn = Button(master=self.frame, text="Change Password", bg=WHITE, fg=BLACK, font=LABEL_12, command=self.change_pwd) #type: ignore

        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        name_label.grid(row=1, column=0, sticky="w")
        self.name_entry.grid(row=1, column=1, pady=10)

        email_label.grid(row=2, column=0,  sticky="w")
        self.email_entry.grid(row=2, column=1,pady=10)

        update_btn.grid(row=3, column=1, sticky="w")

        sub_title_label.grid(row=4, column=0, pady=(40,5), sticky="w")

        current_pwd.grid(row=5, column=0,  sticky="w")
        self.current_entry.grid(row=5, column=1, pady=10)

        password.grid(row=6, column=0,  sticky="w")
        self.password_entry.grid(row=6, column=1, pady=10)

        cpassword.grid(row=7, column=0,  sticky="w")
        self.cpassword_entry.grid(row=7, column=1, pady=10)

        change_pwd_btn.grid(row=8, column=1, sticky="w")


    def update_profile(self):
        new_name = self.name_entry.get().strip()
        new_email = self.email_entry.get().strip().lower()

        if self.user["name"] == new_name and self.user["email"] == new_email:
            return

        try:
            db.update_profile(self.user["id"], new_name, new_email)
        except ProfileError as error:
            mb.showerror("Error", str(error))
            return

        self.user["name"] = new_name
        self.user["email"] = new_email
        mb.showinfo("Success", "Profile updated.")


    def change_pwd(self):
        current_password = self.current_entry.get()
        new_password = self.password_entry.get()
        confirm_password = self.cpassword_entry.get()

        try:
            db.change_password(self.user["id"], current_password, new_password, confirm_password)
        except ProfileError as error:
            mb.showerror("Error", str(error))
            return

        # clear the password entries
        self.current_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.cpassword_entry.delete(0, END)
        mb.showinfo("Success", "Password changed successfully.")