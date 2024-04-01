from datetime import datetime
from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3
import connect_db as connect_db
import base64

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


def waiting_status():
    connection.execute(
        """SELECT Products.product_id,Products.name,Products.description,Products.price,Products.picture ,Order_Details.quantity
        FROM Order_Details 
        INNER JOIN Products 
        on Products.product_id = Order_Details.product_id
        INNER JOIN Orders 
        on Orders.order_id = Order_Details.order_id
        INNER JOIN Customers 
        on Customers.customer_id = Orders.customer_id
        WHERE Orders.customer_id = ? 
        AND  Orders.status = ?
        """,
        (customer_information[0], "Waiting"),
    )
    order_list_waiting = connection.fetchall()
    order_list2_waiting = []
    for order in order_list_waiting:
        order_list2_waiting.append(
            {
                "product_id": order[0],
                "name": order[1],
                "description": order[2],
                "price": order[3],
                "picture": base64.b64encode(order[4]).decode("utf-8"),
                "quantity": order[5],
            }
        )
    return order_list2_waiting


def confirmation_status():
    connection.execute(
        """SELECT Products.product_id,Products.name,Products.description,Products.price,Products.picture ,Order_Details.quantity
        FROM Order_Details 
        INNER JOIN Products 
        on Products.product_id = Order_Details.product_id
        INNER JOIN Orders 
        on Orders.order_id = Order_Details.order_id
        INNER JOIN Customers 
        on Customers.customer_id = Orders.customer_id
        WHERE Orders.customer_id = ? 
        AND  Orders.status = ?
        """,
        (customer_information[0], "Confirmation"),
    )
    order_list_confirmation = connection.fetchall()
    order_list2_confirmation = []
    for order in order_list_confirmation:
        order_list2_confirmation.append(
            {
                "product_id": order[0],
                "name": order[1],
                "description": order[2],
                "price": order[3],
                "picture": base64.b64encode(order[4]).decode("utf-8"),
                "quantity": order[5],
            }
        )
    return order_list2_confirmation


def Send_status():
    connection.execute(
        """SELECT Products.product_id,Products.name,Products.description,Products.price,Products.picture ,Order_Details.quantity
        FROM Order_Details 
        INNER JOIN Products 
        on Products.product_id = Order_Details.product_id
        INNER JOIN Orders 
        on Orders.order_id = Order_Details.order_id
        INNER JOIN Customers 
        on Customers.customer_id = Orders.customer_id
        WHERE Orders.customer_id = ? 
        AND  Orders.status = ?
        """,
        (customer_information[0], "Send"),
    )
    order_list_Send = connection.fetchall()
    order_list2_Send = []
    for order in order_list_Send:
        order_list2_Send.append(
            {
                "product_id": order[0],
                "name": order[1],
                "description": order[2],
                "price": order[3],
                "picture": base64.b64encode(order[4]).decode("utf-8"),
                "quantity": order[5],
            }
        )
    return order_list2_Send


def Delivery_status():
    connection.execute(
        """SELECT Products.product_id,Products.name,Products.description,Products.price,Products.picture ,Order_Details.quantity
        FROM Order_Details 
        INNER JOIN Products 
        on Products.product_id = Order_Details.product_id
        INNER JOIN Orders 
        on Orders.order_id = Order_Details.order_id
        INNER JOIN Customers 
        on Customers.customer_id = Orders.customer_id
        WHERE Orders.customer_id = ? 
        AND  Orders.status = ?
        """,
        (customer_information[0], "Delivery"),
    )
    order_list_Delivery = connection.fetchall()
    order_list2_Delivery = []
    for order in order_list_Delivery:
        order_list2_Delivery.append(
            {
                "product_id": order[0],
                "name": order[1],
                "description": order[2],
                "price": order[3],
                "picture": base64.b64encode(order[4]).decode("utf-8"),
                "quantity": order[5],
            }
        )
    return order_list2_Delivery


@app.route("/order-history/")
def order_history():
    order_list_waiting = waiting_status()
    order_list_confirmation = confirmation_status()
    order_list_send = Send_status()
    order_list_Delivery = Delivery_status()
    return render_template(
        "pages/order-history.html",
        order_list_waiting=order_list_waiting,
        order_list_confirmation=order_list_confirmation,
        order_list_send=order_list_send,
        order_list_Delivery=order_list_Delivery,
    )
