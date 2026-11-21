from tkinter import *
from config import *
import database as db
from tkinter import messagebox as mb
from tkinter import ttk
from abc import ABC, abstractmethod
from database import EmailError


class EmailPage(ABC):
    title = ""
    inbox_or_sent_box = ""
    box_type = ""

    def __init__(self, parent_frame, home):
        self.home = home
        self.user_id = home.user["id"]
        self.frame = Frame(master=parent_frame, bg=BACKGROUND)
        self.frame.pack(fill="both", expand=True, padx=15, pady=15)

        title_label = Label(master=self.frame, text=self.title, bg=BACKGROUND, fg=SIDE_BAR, font=LABEL_16)
        title_label.pack(side="top", anchor="w")

        bottom_bar = Frame(master=self.frame, bg=BACKGROUND)
        bottom_bar.pack(side="bottom", fill="x", pady=(10, 0))

        open_btn = Button(master=bottom_bar, text="Open", bg=WHITE, fg=BLACK, font=LABEL_10, command=self.open_selected_email)
        delete_btn = Button(master=bottom_bar, text="Delete", bg=WHITE, fg=BLACK, font=LABEL_10, command=self.delete_selected_email)
        refresh_btn = Button(master=bottom_bar, text="Refresh", bg=WHITE, fg=BLACK, font=LABEL_10, command=self.display_emails)

        open_btn.pack(side="left", padx=(0,5))
        delete_btn.pack(side="left", padx=5)
        refresh_btn.pack(side="left", padx=5)

        #table
        table_frame = Frame(master=self.frame, background=BACKGROUND)
        table_frame.pack(side="top", fill="both", expand=True, pady=(10, 0))

        self.table = ttk.Treeview(master=table_frame, columns=("person", "subject", "date"), show="headings", selectmode="browse")
        self.table.heading("person", text=self.inbox_or_sent_box)
        self.table.heading("subject", text="Subject")
        self.table.heading("date", text="Date")

        self.table.column("person", width=220)
        self.table.column("subject", width=250)
        self.table.column("date", width=120)

        scrollbar = Scrollbar(master=table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.display_emails()

    @abstractmethod
    def get_emails(self):
        pass

    #this fn load the emails and insert into the Treeview table as rows
    def display_emails(self):
        for row in self.table.get_children():
            self.table.delete(row)

        emails = self.get_emails()
        for email in emails:
            person = f"{email["other_name"]} ({email["other_email"]})"
            self.table.insert("", END, iid=str(email["id"]), values=(person, email["subject"], email["timestamp"]))

    def get_selected_email_id(self):
        rows = self.table.selection()

        if len(rows) == 0:
            mb.showerror("Error", "Pls choose an email first.")
            return None
        return int(rows[0])

    def open_selected_email(self):
        email_id = self.get_selected_email_id()
        if email_id is None:
            return
        self.home.show_email_detail(box_type = self.box_type, email_id=email_id)

    def delete_selected_email(self):
        email_id = self.get_selected_email_id()
        if email_id is None:
            return

        confirm = mb.askyesno("Delete", "Are you sure? Email will be deleted.")
        if confirm == False:
            return

        db.delete_email(email_id=email_id)
        mb.showinfo("Success", "Email has been deleted.")

        self.display_emails()


class InboxPage(EmailPage):
    title = "Inbox"
    inbox_or_sent_box = "From"
    box_type = "inbox"

    def get_emails(self):
        emails = db.get_inbox_mails(self.user_id)
        return emails


class SentPage(EmailPage):
    title = "Sent"
    inbox_or_sent_box = "To"
    box_type = "sent"

    def get_emails(self):
        emails = db.get_sent_mails(self.user_id)
        return emails


class WriteEmail(object):
    def __init__(self, parent_frame, home):
        self.home = home
        self.frame = Frame(master=parent_frame, bg=BACKGROUND)
        self.frame.pack(fill="both", expand=True, padx=15, pady=15)

        title_label = Label(master=self.frame, text="Write Email", bg=BACKGROUND, fg=SIDE_BAR, font=LABEL_16)
        to_label = Label(master=self.frame, text="To: ", bg=BACKGROUND, fg=BLACK, font=LABEL_12)
        subject_label = Label(master=self.frame, text="Subject: ", bg=BACKGROUND, fg=BLACK, font=LABEL_12)
        message_label = Label(master=self.frame, text="Message: ", bg=BACKGROUND, fg=BLACK, font=LABEL_12)

        self.to_entry = Entry(master=self.frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12)
        self.subject_entry = Entry(master=self.frame, bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12)
        self.body_message = Text(master=self.frame, height=12, wrap="word", bg=WHITE, fg=BLACK, insertbackground=BLACK, font=LABEL_12)

        send_btn = Button(master=self.frame, text="Send", bg=WHITE, font=LABEL_12, command=self.send)
        clear_btn = Button(master=self.frame, text="Clear", bg=WHITE, font=LABEL_12, command=self.clear)

        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        to_label.grid(row=1, column=0, pady=5, sticky="w")
        self.to_entry.grid(row=1, column=1, pady=5, sticky="ew")

        subject_label.grid(row=2, column=0, pady=5, sticky="w")
        self.subject_entry.grid(row=2, column=1, pady=5, sticky="ew")

        message_label.grid(row=3, column=0, pady=5, sticky="nw")
        self.body_message.grid(row=3, column=1, pady=5, sticky="nsew")

        send_btn.grid(row=4, column=1, pady=10, sticky="w")
        clear_btn.grid(row=4, column=1, pady=10, sticky="e")

        self.frame.rowconfigure(3, weight=1)
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


class EmailDetail(object):
    def __init__(self, parent_frame, home, box_type, email_id):
        #home is HomeScreen page it contains navigation between inbox, sent, write pages
        self.home = home
        self.user_id = home.user["id"]
        self.email_id = email_id
        self.box_type = box_type

        #Main Frame of email detail
        self.frame = Frame(master=parent_frame, background=BACKGROUND)
        self.frame.pack(fill="both", expand=True, padx=15, pady=15)

        try:
            email = db.get_email_detail(self.email_id)

        except EmailError as e:
            mb.showerror("Error", str(e))
            return

        subject_text = f"Subject: {email["subject"]}"
        from_text = f"From: {email["sender_name"]} ({email["sender_email"]})"
        to_text = f"To: {email["receiver_name"]} ({email["receiver_email"]})"
        date_text = f"Date: {email["timestamp"]}"

        subject_label = Label(master=self.frame, text=subject_text, bg=BACKGROUND, fg=BLACK, font=LABEL_14, anchor="w",)
        from_label = Label(master=self.frame, text=from_text, bg=BACKGROUND, fg=BLACK, font=LABEL_10, anchor="w")
        to_label = Label(master=self.frame, text=to_text, bg=BACKGROUND, fg=BLACK, font=LABEL_10, anchor="w")
        date_label = Label(master=self.frame, text=date_text, bg=BACKGROUND, fg=BLACK, font=LABEL_10, anchor="w")

        subject_label.pack(side="top", fill="x")
        from_label.pack(side="top", fill="x")
        to_label.pack(side="top", fill="x")
        date_label.pack(side="top", fill="x")

        #body frame
        body_frame = Frame(master=self.frame, bg=BACKGROUND)
        body_frame.pack(side="top", fill="both", expand=True)

        body_text = Text(master=body_frame, wrap="word", font=LABEL_12)
        scrollbar = Scrollbar(master=body_frame, orient="vertical", command=body_text.yview)
        body_text.configure(yscrollcommand=scrollbar.set)

        body_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        body_text.insert("1.0", email["body"])
        body_text.configure(state="disabled")

        bottom_frame = Frame(master=self.frame, bg=BACKGROUND)
        bottom_frame.pack(side="bottom", fill="x", pady=(10,0))

        back_btn = Button(master=bottom_frame, text="Back", bg=WHITE, fg=BLACK, command=self.go_back)
        delete_btn = Button(master=bottom_frame, text="Delete", bg=WHITE, fg=BLACK, command=self.delete_email)

        back_btn.pack(side="left", padx=(5,10))
        delete_btn.pack(side="left")

    def go_back(self):
        self.home.clear_content()
        if self.box_type == "inbox":
            self.home.show_inbox()
        else:
            self.home.show_sent_page()


    def delete_email(self):
        confirm = mb.askyesno("Delete", "Are you sure? Email will be deleted.")

        if confirm == False:
            return

        db.delete_email(email_id=self.email_id)
        mb.showinfo("Success", "Email has been deleted.")
        self.go_back()
