from config import *
from tkinter import *


class HomeScreen:
    def __init__(self, parent_window):
        self.home_screen = Frame(master=parent_window, background=BACKGROUND) #type: ignore
        self.home_screen.pack(fill='both', expand=True)

        #top bar
        top_bar = Frame(master=self.home_screen, height=100, background="#aabbcc")
        top_bar.pack(side='top', fill="x")

        #itmes inside topbar
        title_label = Label(master=top_bar, text="Email App", bg="#aabbcc", fg=BLACK, font=LABEL_16) #type: ignore
        title_label.pack(side="left", padx=15)

        profile_btn = Button(master=top_bar, text="👤", bg=WHITE, font=LABEL_12) #type: ignore
        profile_btn.pack(side="right", padx=5, pady=5)

        logout_btn = Button(master=top_bar, text="Logout", bg=WHITE, font=LABEL_12) #type: ignore
        logout_btn.pack(side="right")

        #side bar
        side_bar = Frame(master=self.home_screen, width=150, background="#231245")
        side_bar.pack(side="left", fill="y")

        #items inside sidebar
        write_btn = Button(master=side_bar, text="Write Email", bg=WHITE, font=LABEL_12) #type: ignore
        inbox_btn = Button(master=side_bar, text="Inbox", bg=WHITE, font=LABEL_12) #type: ignore
        sentbox_btn = Button(master=side_bar, text="Sent", bg=WHITE, font=LABEL_12) #type: ignore

        write_btn.pack(fill="x", padx=10, pady=(30, 2))
        inbox_btn.pack(fill="x", padx=10, pady=5)
        sentbox_btn.pack(fill="x", padx=10, pady=5)

        self.content_area = Frame(master=self.home_screen, background=BACKGROUND) #type: ignore
        self.content_area.pack(side="left", fill="both", expand=True)