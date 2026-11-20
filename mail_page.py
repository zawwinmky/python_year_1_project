from tkinter import *
from config import * #type: ignore
import database as db
from tkinter import messagebox as mb

class InboxPage(object):
    def __init__(self, parent_frame):
        self.title = "Inbox"

        self.frame = Frame(master=parent_frame, bg=BACKGROUND) #type: ignore
        self.frame.pack(fill="both", expand=True, padx=15, pady=15)

        title_label = Label(master=self.frame, text=self.title, bg=BACKGROUND, fg=BLACK, font=LABEL_16) #type: ignore
        title_label.pack(side="top", anchor="e")

        bottom_bar = Frame(master=self.frame, bg=BACKGROUND) #type: ignore
        bottom_bar.pack(side="bottom", fill="x", pady=(10, 0))

        open_btn = Button(master=bottom_bar, text="Open", bg=WHITE, fg=BLACK, font=LABEL_10) #type: ignore
        delete_btn = Button(master=bottom_bar, text="Delete", bg=WHITE, fg=BLACK, font=LABEL_10) #type: ignore
        refresh_btn = Button(master=bottom_bar, text="Refresh", bg=WHITE, fg=BLACK, font=LABEL_10) #type: ignore

        open_btn.pack(side="left", padx=(0,5))
        delete_btn.pack(side="left", padx=5)
        refresh_btn.pack(side="left", padx=5)


class SentPage(object):
    def __init__(self, parent_frame):
        self.title = "Sent"

        self.frame = Frame(master=parent_frame, bg=BACKGROUND) #type: ignore
        self.frame.pack(fill="both", expand=True, padx=15, pady=15)

        title_label = Label(master=self.frame, text=self.title, bg=BACKGROUND, fg=BLACK, font=LABEL_16) #type: ignore
        title_label.pack(side="top", anchor="e")

        bottom_bar = Frame(master=self.frame, bg=BACKGROUND) #type: ignore
        bottom_bar.pack(side="bottom", fill="x", pady=(10, 0))

        open_btn = Button(master=bottom_bar, text="Open", bg=WHITE, fg=BLACK, font=LABEL_10) #type: ignore
        delete_btn = Button(master=bottom_bar, text="Delete", bg=WHITE, fg=BLACK, font=LABEL_10) #type: ignore
        refresh_btn = Button(master=bottom_bar, text="Refresh", bg=WHITE, fg=BLACK, font=LABEL_10) #type: ignore

        open_btn.pack(side="left", padx=(0,5))
        delete_btn.pack(side="left", padx=5)
        refresh_btn.pack(side="left", padx=5)


class WriteEmail(object):
    def __init__(self, parent_frame, home):
        self.home = home
        self.frame = Frame(master=parent_frame, bg=BACKGROUND) #type: ignore
        self.frame.pack(fill="both", expand=True, padx=15, pady=15)

        title_label = Label(master=self.frame, text="Write Email", bg=BACKGROUND, fg=BLACK, font=LABEL_16) #type: ignore
        to_label = Label(master=self.frame, text="To: ", bg=BACKGROUND, fg=BLACK, font=LABEL_12) #type: ignore
        subject_label = Label(master=self.frame, text="Subject: ", bg=BACKGROUND, fg=BLACK, font=LABEL_12) #type: ignore
        message_label = Label(master=self.frame, text="Message: ", bg=BACKGROUND, fg=BLACK, font=LABEL_12) #type: ignore

        self.to_entry = Entry(master=self.frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.subject_entry = Entry(master=self.frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore
        self.body_message = Text(master=self.frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12) #type: ignore

        send_btn = Button(master=self.frame, text="Send", bg=WHITE, font=LABEL_12, command=self.send) #type: ignore
        clear_btn = Button(master=self.frame, text="Clear", bg=WHITE, font=LABEL_12, command=self.clear) #type: ignore

        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        to_label.grid(row=1, column=0, pady=5, sticky="w")
        self.to_entry.grid(row=1, column=1, pady=5, sticky="w")

        subject_label.grid(row=2, column=0, pady=5, sticky="w")
        self.subject_entry.grid(row=2, column=1, pady=5, sticky="w")

        message_label.grid(row=3, column=0, pady=5, sticky="nw")
        self.body_message.grid(row=3, column=1, pady=5, sticky="nsew")

        send_btn.grid(row=4, column=1, pady=10, sticky="w")
        clear_btn.grid(row=4, column=1, pady=10, sticky="e")

        self.frame.rowconfigure(4, weight=1)
        self.frame.columnconfigure(1, weight=1)


    def clear(self):
        self.to_entry.delete(0, END)
        self.subject_entry.delete(0, END)
        self.body_message.delete("1.0", END)

    def send(self):
        email = self.to_entry.get().strip().lower()
        subject = self.subject_entry.get().strip()
        body_message = self.body_message.get("1.0", END).strip()

        try:
            db.send_email(sender_id=self.home.user["id"], receiver_email=email, subject = subject, body_message=body_message)
        except Exception as e:
            mb.showerror("Error", str(e))
            return

        mb.showinfo("Success", "Email sent successfully!")
        self.home.write_email()