from config import * #type: ignore
from tkinter import *
from login_page import LoginPage, RegisterPage #type: ignore
from home_page import HomeScreen #type: ignore

def main():
    base_window = Tk()
    base_window.title("Email app")
    base_window.geometry("800x800")
    base_window.config(bg=BACKGROUND) #type: ignore

    #login_page = LoginPage(base_window)
    register_page = RegisterPage(base_window)
    #home_screen = HomeScreen(base_window)

    base_window.mainloop()




if __name__ == "__main__":
    main()