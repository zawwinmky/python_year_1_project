import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash #type: ignore


FOLDER = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(FOLDER, "email_app.db")


class DatabaseError(Exception):
    pass

class RegisterError(Exception):
    pass

class LoginError(Exception):
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
    name = name.strip()
    email = email.strip().lower()

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
    email = email.strip().lower()
    password = password

    if email == "" or password == "":
        raise LoginError("Enter your email and password!")

    user = find_user_by_email(email=email)

    if user is None:
        raise LoginError("Invalid email or password.")

    if not check_password_hash(user["password"], password):
        raise LoginError("Invalid email or password!")

    return user