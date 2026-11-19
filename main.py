from config import * #type: ignore
from tkinter import *
from login_page import LoginPage, RegisterPage #type: ignore
from home_page import HomeScreen #type: ignore
import database as db

def main():
    db.create_tables()

    base_window = Tk()
    base_window.title("Email app")
    base_window.geometry("800x800")
    base_window.config(bg=BACKGROUND) #type: ignore

    app = App(base_window)
    app.login_page()

    base_window.mainloop()

class App(object):
    def __init__(self, window):
        self.window = window


    def home_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        HomeScreen(self.window, app=self)


    def login_page(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        LoginPage(self.window, app=self)

    def register_page(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        RegisterPage(self.window, app=self)

    def logout(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        LoginPage(self.window, app=self)

if __name__ == "__main__":
    main()