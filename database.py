import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash #type: ignore
from datetime import datetime as dt


FOLDER = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(FOLDER, "email_app.db")


class AppError(Exception):
    pass

class RegisterError(AppError):
    pass

class LoginError(AppError):
    pass

class ProfileError(AppError):
    pass

class EmailError(AppError):
    pass


def create_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    user_table = """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL )
            """
    cursor.execute(user_table)

    email_table = """
            CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender INTEGER NOT NULL,
            receiver INTEGER NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (sender) REFERENCES users (id),
            FOREIGN KEY (receiver) REFERENCES users (id) )
            """

    cursor.execute(email_table)

    connection.commit()
    connection.close()

def find_user_by_email(email):
    connection = create_connection()
    cursor = connection.cursor()
    command = "SELECT * FROM users WHERE email = ?"
    cursor.execute(command, (email,))
    user = cursor.fetchone()
    connection.close()
    return user


def add_user(name, email, password, cpassword):
    if name == "" or email == "" or password == "" or cpassword == "":
        raise RegisterError("Pls fill in all fields!")

    if len(password) < 6:
        raise RegisterError("Password must be at least 6 characters!")

    if password != cpassword:
        raise RegisterError("Passwords do not match!")

    user = find_user_by_email(email=email)

    if user is not None:
        raise RegisterError("Email has been used already.")

    password_hash = generate_password_hash(password)

    connection = create_connection()
    cursor = connection.cursor()

    command = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)"
    cursor.execute(command, (name, email, password_hash))

    connection.commit()
    connection.close()


def check_login(email, password):
    if email == "" or password == "":
        raise LoginError("Enter your email and password!")

    user = find_user_by_email(email=email)

    if user is None:
        raise LoginError("Invalid email or password.")

    if not check_password_hash(user["password"], password):
        raise LoginError("Invalid email or password!")

    return user


def update_profile(user_id, new_name, new_email):
    """Change the name and email of a user. Raises a ProfileError if something is wrong."""

    if new_name == "" or new_email == "":
        raise ProfileError("Name and email cannot be empty.")

    # check email is used or not
    other_user = find_user_by_email(new_email)
    if other_user is not None and other_user["id"] != user_id:
        raise ProfileError("Email already used!")

    connection = create_connection()
    cursor = connection.cursor()
    command = "UPDATE users SET name = ?, email = ? WHERE id = ?"
    cursor.execute(command,(new_name, new_email, user_id))
    connection.commit()
    connection.close()

def find_user_by_id(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    command = "SELECT * FROM users where id = ?"
    cursor.execute(command, (user_id,))
    user = cursor.fetchone()
    connection.close()
    return user

def change_password(user_id, current_password, new_password, confirm_password):
    if current_password == "" or new_password == "" or confirm_password == "":
        raise ProfileError("Please fill in all password fields.")

    user = find_user_by_id(user_id)
    if user is None:
        raise ProfileError("User not found.")

    if not check_password_hash(user["password"], current_password):
        raise ProfileError("Incorrect current password.")

    if len(new_password) < 6:
        raise ProfileError("New password must be at least 6 characters.")

    if new_password != confirm_password:
        raise ProfileError("New passwords do not match.")

    new_hash = generate_password_hash(new_password)

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_hash, user_id))
    connection.commit()
    connection.close()

def send_email(sender_id,receiver_email, subject, body_message):

    if receiver_email == "" or subject == "" or body_message == "":
        raise EmailError("Pls fill in all the required")

    receiver = find_user_by_email(receiver_email)

    if receiver is None:
        raise EmailError("There is no user with that email.")

    time = dt.now()

    connection = create_connection()
    cursor = connection.cursor()
    command = "INSERT INTO emails (sender, receiver, subject, body, timestamp) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(command, (sender_id, receiver["id"], subject, body_message, time))
    connection.commit()
    connection.close()


def get_inbox_mails(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    inbox_command ="""
                    SELECT emails.id, emails.subject, emails.timestamp,
                    users.name AS other_name, users.email AS other_email
                    FROM emails
                    JOIN users ON emails.sender = users.id
                    WHERE emails.receiver = ?
                    ORDER BY emails.id DESC """

    cursor.execute(inbox_command, (user_id,))
    emails = cursor.fetchall()
    connection.close()
    return emails


def get_sent_mails(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    sent_box ="""
                SELECT emails.id, emails.subject, emails.timestamp,
                users.name AS other_name, users.email AS other_email
                FROM emails
                JOIN users ON emails.receiver = users.id
                WHERE emails.sender = ?
                ORDER BY emails.id DESC """

    cursor.execute(sent_box, (user_id,))
    emails = cursor.fetchall()
    connection.close()
    return emails
