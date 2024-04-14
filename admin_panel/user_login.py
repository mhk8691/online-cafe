from flask import Flask, request, jsonify, json, redirect, url_for, render_template


import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re
app = connect_db.app

user_information = []


def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/admin/", methods=["POST", "GET"])
def login_admin():
    user_information.clear()

    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur.execute(
            "select * from Users where username = ? and password = ?",
            (
                username,
                password,
            ),
        )
        login_list = cur.fetchone()
        if login_list is None:
            return redirect(url_for("login_admin"))

        else:
            for login in login_list:
                user_information.append(login)
            return redirect("http://localhost:5173")

    return render_template("pages/user-login.html")
