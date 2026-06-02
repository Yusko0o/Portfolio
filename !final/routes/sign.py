from flask import Blueprint, request
import sqlite3
import hashlib as h
import os

sign = Blueprint("sign", __name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "users.db")

@sign.route("/sign_in", methods=["POST"])
def sign_in():
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Missing email or password"

        hashPassword = h.sha1(password.encode()).hexdigest()

        connect = sqlite3.connect(DB_PATH)
        cursor= connect.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing = cursor.fetchone()

        if existing:
            return "Email already exisits"

        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashPassword)
        )

        connect.commit()
        connect.close()

        return "User created ! You can now log in !"
    
    except Exception as e:
        return f"Error : {e}"