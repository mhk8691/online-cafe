from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re

app = connect_db.app


cors = CORS(app)
app.config["UPLOAD_FOLDER"] = "static/img/"

text = "Super Admin"

def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


time = datetime.today().strftime("%Y-%m-%d")


def admin_log(user_id, action, action_date, ip_address):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Admin_Logs (user_id,action,action_date,ip_address) VALUES (?,?,?,?)",
        (
            user_id,
            action,
            action_date,
            ip_address,
        ),
    )
    conn.commit()
    conn.close()


# Get a customer by ID
def get_customer(customer_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
    customer = cur.fetchone()
    final_customer = {
        "id": customer[0],
        "username": customer[1],
        "password": customer[2],
        "email": customer[3],
        "phone": customer[4],
    }
    conn.close()
    return final_customer


# Create a new customer
def create_customer(name, password, email, phone, registration_date):
    if text == "Admin" or text == "Super Admin":

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customers (username,password, email, phone,registration_date) VALUES (?, ?, ?,?,?)",
            (name, password, email, phone, registration_date),
        )
        conn.commit()
        customer_id = cur.lastrowid
        conn.close()
        return customer_id


# Update a customer
def update_customer(customer_id, name, password, email, phone):
    if text == "Admin" or text == "Super Admin":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE customers SET username = ?,password = ?, email = ?, phone = ? WHERE customer_id = ?",
            (name, password, email, phone, customer_id),
        )
        conn.commit()
        conn.close()
        return get_customer(customer_id)


# Delete a customer
def delete_customer(customer_id):
    if text == "Admin" or text == "Super Admin":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
        cur.execute("DELETE FROM Shipping_Addresses WHERE customer_id = ?", (customer_id,))
        cur.execute("DELETE FROM Feedback WHERE customer_id = ?", (customer_id,))
        cur.execute("DELETE FROM cart WHERE customer_id = ?", (customer_id,))
        conn.commit()
        conn.close()


# Get all customers
def get_all_customers(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM customers LIMIT ?",
        (str(limit),),
    )
    customers = cur.fetchall()
    final_customers = []
    for customer in customers:
        final_customers.append(
            {
                "id": customer[0],
                "username": customer[1],
                "password": customer[2],
                "email": customer[3],
                "phone": customer[4],
            }
        )
    conn.close()
    return final_customers


def get_all_customers_filter(name, search, limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM customers   WHERE {name} = ? LIMIT {limit}",
        (search,),
    )
    customers = cur.fetchall()
    final_customers = []
    for customer in customers:
        final_customers.append(
            {
                "id": customer[0],
                "username": customer[1],
                "password": customer[2],
                "email": customer[3],
                "phone": customer[4],
            }
        )
    conn.close()
    return final_customers


# CRUD routes
@app.route("/customer/", methods=["GET"])
def list_customer():
    range = request.args.get("range")
    x = re.split(",", range)
    final_range = re.split("]", x[1])[0]
    get_filter = request.args.get("filter")
    customers = get_all_customers(int(final_range) + 1)
    response = jsonify(customers)
    if len(get_filter) > 2:
        name = re.split(r""":""", get_filter)
        name2 = re.split(r"""^{\"""", name[0])
        name2 = re.split(r"""\"$""", name2[1])
        regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

        response = jsonify(
            get_all_customers_filter(
                name2[0],
                regex_filter[1],
                int(final_range) + 1,
            ),
        )

    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(customers)

    return response


@app.route("/customer", methods=["POST"])
def add_customer():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]
    phone = request.json["phone"]
    user_ip = request.remote_addr

    action = f"Add user: {name}"
    admin_log(3, action, time, user_ip)
    customer_id = create_customer(name, password, email, phone, time)
    return jsonify(get_customer(customer_id)), 201


@app.route("/customer/<int:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customer = get_customer(customer_id)
    if customer is None:
        return "", 404
    return jsonify(customer), 200


@app.route("/customer/<int:customer_id>", methods=["PUT"])
def update_customer_by_id(customer_id):
    name = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    phone = request.json["phone"]
    user_ip = request.remote_addr

    updated = update_customer(customer_id, name, password, email, phone)
    action = f"Update user: {name}"
    admin_log(3, action, time, user_ip)
    return jsonify(updated), 200


def get_username(customer_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT username from Customers where customer_id = ?", (customer_id,))
    username = cur.fetchone()

    for user in username:
        final_username = user
    return final_username


@app.route("/customer/<int:customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id):
    username = get_username(customer_id)
    user_ip = request.remote_addr

    delete_customer(customer_id)
    action = f"Delete user: {username}"
    admin_log(3, action, time, user_ip)
    return jsonify({"id": customer_id}), 200
