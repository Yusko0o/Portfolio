from flask import Blueprint, render_template, request
import sqlite3
import hashlib as h
import os

auth = Blueprint("auth", __name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "users.db")

@auth.route("/log_in", methods=["GET"])
def login_page():
    return render_template("index.html")

@auth.route("/log_in", methods=["POST"])
def login():
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        hashPassword = h.sha1(password.encode()).hexdigest()

        connect = sqlite3.connect(DB_PATH)
        cursor= connect.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()
        connect.close()

        if not user:
            return "No account"

        if user[0] == hashPassword:
            return "You're logged in !"
        else:
            return "Incorrect !"
    except Exception as e:
        return f"Error: {e}"