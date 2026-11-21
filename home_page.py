from config import * # type: ignore
from tkinter import *
from profile_page import ProfilePage
from mail_page import InboxPage, SentPage, WriteEmail, EmailDetail #type: ignore

class HomeScreen(object):
    def __init__(self, parent_window, app):
        self.app = app
        self.user = app.current_user
        self.home_screen_frame = Frame(master=parent_window, background=BACKGROUND) #type: ignore
        self.home_screen_frame.pack(fill='both', expand=True)

        #top bar
        top_bar_frame = Frame(master=self.home_screen_frame, height=100, background=TOP_BAR_BG) #type: ignore
        top_bar_frame.pack(side='top', fill="x")

        #itmes inside topbar
        title_label = Label(master=top_bar_frame, text="Email App", bg=TOP_BAR_BG, fg=BLACK, font=LABEL_16) #type: ignore
        title_label.pack(side="left", padx=15)

        profile_btn = Button(master=top_bar_frame, text="👤", bg=WHITE, font=LABEL_12, command=self.profile) #type: ignore
        profile_btn.pack(side="right", padx=(5,15), pady=5)

        logout_btn = Button(master=top_bar_frame, text="Logout", bg=WHITE, font=LABEL_12, command=self.app.logout) #type: ignore
        logout_btn.pack(side="right")

        #side bar
        side_bar_frame = Frame(master=self.home_screen_frame, width=150, background=SIDE_BAR) #type: ignore
        side_bar_frame.pack(side="left", fill="y")

        #items inside sidebar
        write_btn = Button(master=side_bar_frame, text="Write Email", bg=WHITE, font=LABEL_12, command=self.write_email) #type: ignore
        inbox_btn = Button(master=side_bar_frame, text="Inbox", bg=WHITE, font=LABEL_12, command=self.show_inbox) #type: ignore
        sentbox_btn = Button(master=side_bar_frame, text="Sent", bg=WHITE, font=LABEL_12, command=self.show_sent_page) #type: ignore

        write_btn.pack(fill="x", padx=10, pady=(30, 5))
        inbox_btn.pack(fill="x", padx=10, pady=5)
        sentbox_btn.pack(fill="x", padx=10, pady=5)

        self.content_area = Frame(master=self.home_screen_frame, background=BACKGROUND) #type: ignore
        self.content_area.pack(side="left", fill="both", expand=True)

        self.show_inbox()

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def profile(self):
        self.clear_content()
        ProfilePage(parent_frame=self.content_area, user=self.app.current_user)

    def show_inbox(self):
        self.clear_content()
        InboxPage(parent_frame=self.content_area, home=self)

    def show_sent_page(self):
        self.clear_content()
        SentPage(parent_frame=self.content_area, home=self)

    def write_email(self):
        self.clear_content()
        WriteEmail(parent_frame=self.content_area, home=self)

    def show_email_detail(self, box_type, email_id):
        self.clear_content()
        EmailDetail(parent_frame=self.content_area, home=self, box_type=box_type, email_id=email_id)
