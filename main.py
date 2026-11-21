from config import * #type: ignore
from tkinter import *
from login_page import LoginPage, RegisterPage #type: ignore
from home_page import HomeScreen #type: ignore
import database as db

def main():
    db.create_tables()

    base_window = Tk()
    base_window.title("Email app")
    base_window.geometry("1000x800")
    base_window.config(bg=BACKGROUND) #type: ignore

    app = App(window=base_window)
    app.login_page()

    base_window.mainloop()

class App(object):
    def __init__(self, window):
        self.window = window
        self.current_user = None

    def home_screen(self, user):
        self.current_user = user
        self.clear_screen()
        HomeScreen(parent_window=self.window, app=self)

    def login_page(self):
        self.clear_screen()
        LoginPage(parent_window=self.window, app=self)

    def register_page(self):
        self.clear_screen()
        RegisterPage(parent_window=self.window, app=self)

    def logout(self):
        self.clear_screen()
        self.current_user = None
        LoginPage(parent_window=self.window, app=self)

    def clear_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    main()