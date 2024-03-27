from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import os
import json
import base64
import requests
from werkzeug.utils import secure_filename

app = connect_db.app

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


# ------------------ User Section start---------------
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
    customers = get_all_customers(int(range[3]) + 1)
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


# ------------------ User Section end---------------


# ------------------ Product Section start---------------
# Get a product by ID
def get_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Products WHERE product_id = ?", (product_id,))

    product = cur.fetchone()

    final_product = {
        "id": product[0],
        "name": product[1],
        "description": product[2],
        "price": product[3],
        "categories_id": product[4],
        # "picture": product[4],
    }
    print(final_product["categories_id"])

    conn.close()
    return final_product


# Get all products
def get_all_product(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Products LIMIT " + str(limit))
    products = cur.fetchall()
    final_products = []
    for product in products:
        final_products.append(
            {
                "id": product[0],
                "name": product[1],
                "description": product[2],
                "price": product[3],
                "categories_id": product[5],
                # "picture": product[4],
            }
        )
    conn.close()
    return final_products


# Create a new product
def create_product(name, description, price, categories_id, picture):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Products (name,description, price,categories_id,picture) VALUES (?, ?, ?,?,?)",
        (name, description, price, categories_id, picture),
    )
    conn.commit()
    product_id = cur.lastrowid
    conn.close()
    return product_id


# Update a product
def update_product(product_id, name, description, price, categories_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE products SET name = ?,description = ?, price = ?,categories_id = ? WHERE product_id = ?",
        (name, description, price, categories_id, product_id),
    )
    conn.commit()
    conn.close()
    return get_product(product_id)


# Delete a product
def delete_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()


# CRUD routes
@app.route("/product/", methods=["GET"])
def list_product():
    range = request.args.get("range")
    products = get_all_product(int(range[3]) + 1)
    response = jsonify(products)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(products)
    return response


@app.route("/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    categories_id = request.json["categories_id"]

    picture = request.json["picture"]
    # print(picture["src"])

    product_id = create_product(
        name, description, price, categories_id, "picture.read()"
    )
    return jsonify(get_product(product_id)), 201


@app.route("/product/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    product = get_product(product_id)
    if product is None:
        return "", 404
    return jsonify(product), 200


@app.route("/product/<int:product_id>", methods=["PUT"])
def update_product_by_id(product_id):
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    categories_id = request.json["categories_id"]

    updated = update_product(product_id, name, description, price, categories_id)
    return jsonify(updated), 200


@app.route("/product/<int:product_id>", methods=["DELETE"])
def delete_product_by_id(product_id):
    delete_product(product_id)
    return jsonify({"id": product_id}), 200


# ------------------ Product Section end---------------


# ------------------ Categories Section start---------------
# Get a product by ID
def get_category(category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Categories WHERE category_id = ?", (category_id,))

    category = cur.fetchone()

    final_category = {
        "id": category[0],
        "name": category[1],
        "description": category[2],
        "parent_category_id": category[3],
        "created_at": category[4],
        # "picture": category[5],
    }

    conn.close()
    return final_category


# Get all products
def get_all_category(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Categories LIMIT " + str(limit))
    categories = cur.fetchall()
    final_categories = []
    for category in categories:
        final_categories.append(
            {
                "id": category[0],
                "name": category[1],
                "description": category[2],
                "parent_category_id": category[3],
                "created_at": category[4],
                # "picture": category[5],
            }
        )
    conn.close()
    return final_categories


# Create a new product
def create_category(name, description, parent_category_id, created_at, picture):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Categories (name,description, parent_category_id,created_at,picture) VALUES (?, ?, ?,?,?)",
        (name, description, parent_category_id, created_at, picture),
    )
    conn.commit()
    category_id = cur.lastrowid
    conn.close()
    return category_id


# Update a product
def update_category(name, description, parent_category_id, category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Categories SET name = ?,description = ?, parent_category_id = ? WHERE category_id = ?",
        (name, description, parent_category_id, category_id),
    )
    conn.commit()
    conn.close()
    return get_category(category_id)


# Delete a product
def delete_category(category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Categories WHERE category_id = ?", (category_id,))
    conn.commit()
    conn.close()


# CRUD routes
@app.route("/category/", methods=["GET"])
def list_category():
    range = request.args.get("range")
    categories = get_all_category(int(range[3]) + 1)
    response = jsonify(categories)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(categories)
    return response


@app.route("/category", methods=["POST"])
def add_category():
    name = request.json["name"]
    description = request.json["description"]
    parent_category_id = request.json["parent_category_id"]

    picture = request.json["picture"]
    time = datetime.today().strftime("%Y-%m-%d")

    category_id = create_category(
        name, description, parent_category_id, time, "picture.read()"
    )
    return jsonify(get_category(category_id)), 201


@app.route("/category/<int:category_id>", methods=["GET"])
def get_category_by_id(category_id):
    category = get_category(category_id)
    if category is None:
        return "", 404
    return jsonify(category), 200


@app.route("/category/<int:category_id>", methods=["PUT"])
def update_category_by_id(category_id):
    name = request.json["name"]
    description = request.json["description"]
    parent_category_id = request.json["parent_category_id"]

    updated = update_category(name, description, parent_category_id, category_id)
    return jsonify(updated), 200


@app.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category_by_id(category_id):
    delete_category(category_id)
    return jsonify({"id": category_id}), 200


# ------------------ Categories Section end---------------
