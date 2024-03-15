from datetime import datetime
from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3
import connect_db

app = connect_db.app

customer_information = []

# Connect to the database
conn = sqlite3.connect("onlineShop.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
connection = conn.cursor()


# login user
@app.route("/", methods=["POST", "GET"])
def login():
    customer_information.clear()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection.execute(
            "SELECT customer_id,username,password,email,phone FROM Customers WHERE username = '"
            + username
            + "' AND password = '"
            + password
            + "' "
        )

        rows = connection.fetchone()
        if rows is None:
            return redirect(url_for("login"))
        else:

            for customer in rows:
                customer_information.append(customer)
            return redirect(url_for("home"))

    return render_template("pages/login.html")


# signup user
@app.route("/signup/", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        time = datetime.today().strftime("%Y-%m-%d")
        connection.execute(
            "SELECT username FROM Customers WHERE username = '" + username + "'  "
        )
        register = connection.fetchall()
        if len(register) == 0:
            connection.execute(
                "INSERT INTO Customers (username, password,email,phone,registration_date) VALUES (?, ?,?,?,?)",
                (username, password, email, phone_number, time),
            )
            conn.commit()
            return redirect(url_for("login"))
        else:
            return render_template("pages/signup.html", text="username is tekrari")

    return render_template("pages/signup.html")


# profile user
@app.route("/profile/", methods=["POST", "GET"])
def profile():

    if len(customer_information) == 0:
        return redirect(url_for("login"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]
        id = customer_information[0]
        id2 = str(id)
        connection.execute(
            "UPDATE Customers SET username = '"
            + username
            + "' ,  password = '"
            + password
            + "' ,  email = '"
            + email
            + "' ,  phone = '"
            + phone
            + "' where customer_id = '"
            + id2
            + "' "
        )
        conn.commit()
        connection.execute(
            "select customer_id,username,password,email,phone from Customers where customer_id = '"
            + id2
            + "' "
        )
        list = connection.fetchone()
        customer_information.clear()
        for customer in list:
            customer_information.append(customer)
        print(customer_information[0])
    return render_template(
        "pages/profile.html", customer_information=customer_information
    )


@app.route("/rest-password/", methods=["POST", "GET"])
def reset_password():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        connection.execute(
            "SELECT username FROM Customers WHERE username= '" + username + "' "
        )

        row = connection.fetchone()

        if row is None:
            redirect(url_for("login"))

        else:
            connection.execute(
                "UPDATE Customers SET password = '"
                + password
                + "' where username = '"
                + username
                + "' "
            )
            conn.commit()
            return redirect(url_for("profile"))
    return render_template("pages/reset_password.html")
