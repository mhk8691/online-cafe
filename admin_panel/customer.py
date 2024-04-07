from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re

app = connect_db.app


cors = CORS(app)
app.config["UPLOAD_FOLDER"] = "static/img/"


def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


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
    cur.execute("SELECT * FROM customers LIMIT " + str(limit))
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
    customers = get_all_customers(int(final_range) + 1)
    response = jsonify(customers)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(customers)
    return response


@app.route("/customer", methods=["POST"])
def add_customer():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]
    phone = request.json["phone"]
    time = datetime.today().strftime("%Y-%m-%d")

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
    updated = update_customer(customer_id, name, password, email, phone)
    return jsonify(updated), 200


@app.route("/customer/<int:customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id):
    delete_customer(customer_id)
    return jsonify({"id": customer_id}), 200
