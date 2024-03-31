from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import os
import base64
import requests

app = connect_db.app


cors = CORS(app)
app.config["UPLOAD_FOLDER"] = "static/img/"


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
    # picture_base64 = base64.b64encode(product[4]).decode("utf-8")
    test = product[4]
    print(test)
    cur.execute(
        "SELECT Categories.name FROM Categories inner join Products on Categories.category_id = Products.category_id where Products.category_id = ?",
        (test,),
    )
    t = cur.fetchone()
    final_product = {
        "id": product[0],
        "name": product[1],
        "description": product[2],
        "price": product[3],
        "categories_id": t[0],
        # "picture": picture_base64,
    }

    conn.close()
    return final_product


# Get all products
def get_all_product(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Products LIMIT '" + str(limit) + "' ")
    products = cur.fetchall()
    final_products = []
    for product in products:
        # picture_base64 = base64.b64encode(product[4]).decode("utf-8")

        final_products.append(
            {
                "id": product[0],
                "name": product[1],
                "description": product[2],
                "price": product[3],
                # "picture": picture_base64,
                "categories_id": product[5],
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
    file = request.json["pictures"]

    product_id = create_product(name, description, price, categories_id, "filename")
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


# ------------------ Shipping Addresses Section start---------------
# Get a shipping by ID
def get_shipping(address_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Shipping_Addresses WHERE address_id = ?", (address_id,))

    shipping = cur.fetchone()

    final_shipping = {
        "address_id": shipping[0],
        "customer_id": shipping[1],
        "recipient_name": shipping[2],
        "address_line1": shipping[3],
        "address_line2": shipping[4],
        "city": shipping[5],
        "state": shipping[6],
        "postal_code": shipping[7],
        "country": shipping[8],
    }

    conn.close()
    return final_shipping


# Get all shipping
def get_all_shipping(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Shipping_Addresses LIMIT " + str(limit))
    shippings = cur.fetchall()
    final_shipping = []
    for shipping in shippings:
        final_shipping.append(
            {
                "address_id": shipping[0],
                "customer_id": shipping[1],
                "recipient_name": shipping[2],
                "address_line1": shipping[3],
                "address_line2": shipping[4],
                "city": shipping[4],
                "state": shipping[4],
                "postal_code": shipping[4],
                "country": shipping[4],
            }
        )
    conn.close()
    return final_shipping


# Create a new shipping
def create_shipping(
    customer_id,
    recipient_name,
    address_line1,
    address_line2,
    city,
    state,
    postal_code,
    country,
):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Shipping_Addresses (customer_id,recipient_name, address_line1,address_line2,city,state,postal_code,country) VALUES (?, ?, ?,?,?,?,?,?)",
        (
            customer_id,
            recipient_name,
            address_line1,
            address_line2,
            city,
            state,
            postal_code,
            country,
        ),
    )
    conn.commit()
    address_id = cur.lastrowid
    conn.close()
    return address_id


# Update a shipping
def update_shipping(
    customer_id,
    recipient_name,
    address_line1,
    address_line2,
    city,
    state,
    postal_code,
    country,
    address_id,
):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Shipping_Addresses SET customer_id = ?,recipient_name = ?, address_line1 = ?, address_line2 = ?, city = ?, state = ?, postal_code = ?, country = ? WHERE address_id = ?",
        (
            customer_id,
            recipient_name,
            address_line1,
            address_line2,
            city,
            state,
            postal_code,
            country,
            address_id,
        ),
    )
    conn.commit()
    conn.close()
    return get_shipping(address_id)


# Delete a shipping
def delete_shipping(address_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Shipping_Addresses WHERE address_id = ?", (address_id,))
    conn.commit()
    conn.close()


# CRUD routes
@app.route("/shipping/", methods=["GET"])
def list_shipping():
    range = request.args.get("range")
    shippings = get_all_shipping(int(range[3]) + 1)
    response = jsonify(shippings)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(shippings)
    return response


@app.route("/shipping", methods=["POST"])
def add_shipping():
    customer_id = request.json["customer_id"]
    recipient_name = request.json["recipient_name"]
    address_line1 = request.json["address_line1"]
    address_line2 = request.json["address_line2"]
    city = request.json["city"]
    state = request.json["state"]
    postal_code = request.json["postal_code"]
    country = request.json["country"]

    shipping_id = create_shipping(
        customer_id,
        recipient_name,
        address_line1,
        address_line2,
        city,
        state,
        postal_code,
        country,
    )
    return jsonify(get_shipping(shipping_id)), 201


@app.route("/shipping/<int:address_id>", methods=["GET"])
def get_shipping_by_id(address_id):
    shipping = get_shipping(address_id)
    if shipping is None:
        return "", 404
    return jsonify(shipping), 200


@app.route("/shipping/<int:address_id>", methods=["PUT"])
def update_shipping_by_id(address_id):
    customer_id = request.json["customer_id"]
    recipient_name = request.json["recipient_name"]
    address_line1 = request.json["address_line1"]
    address_line2 = request.json["address_line2"]
    city = request.json["city"]
    state = request.json["state"]
    postal_code = request.json["postal_code"]
    country = request.json["country"]

    updated = update_shipping(
        customer_id,
        recipient_name,
        address_line1,
        address_line2,
        city,
        state,
        postal_code,
        country,
        address_id,
    )
    return jsonify(updated), 200


@app.route("/shipping/<int:address_id>", methods=["DELETE"])
def delete_shipping_by_id(address_id):
    delete_shipping(address_id)
    return jsonify({"id": address_id}), 200


# ------------------ Shipping Addresses Section end---------------


# Get a user by ID
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))

    user = cur.fetchone()

    final_user = {
        "user_id": user[0],
        "username": user[1],
        "password": user[2],
        "email": user[3],
        "role": user[4],
    }

    conn.close()
    return final_user


# Get all user
def get_all_user(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users LIMIT " + str(limit))
    users = cur.fetchall()
    final_users = []
    for user in users:
        final_users.append(
            {
                "user_id": user[0],
                "username": user[1],
                "password": user[2],
                "email": user[3],
                "role": user[4],
            }
        )
    conn.close()
    return final_users


# Create a new user
def create_user(
    username,
    password,
    email,
    role,
):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Users (username,password, email,role) VALUES (?, ?, ?,?)",
        (
            username,
            password,
            email,
            role,
        ),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


# Update a user
def update_user(
    username,
    password,
    email,
    role,
    user_id,
):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Users SET username = ?,password = ?, email = ?, role = ? WHERE user_id = ?",
        (
            username,
            password,
            email,
            role,
            user_id,
        ),
    )
    conn.commit()
    conn.close()
    return get_user(user_id)


# Delete a user
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# CRUD routes
@app.route("/user/", methods=["GET"])
def list_user():
    range = request.args.get("range")
    users = get_all_user(int(range[3]) + 1)
    response = jsonify(users)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(users)
    return response


@app.route("/user", methods=["POST"])
def add_user():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    role = request.json["role"]

    userlist = create_user(
        username,
        password,
        email,
        role,
    )
    return jsonify(get_user(userlist)), 201


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = get_user(user_id)
    if user is None:
        return "", 404
    return jsonify(user), 200


@app.route("/user/<int:user_id>", methods=["PUT"])
def update_user_by_id(user_id):
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    role = request.json["role"]

    updated = update_user(
        username,
        password,
        email,
        role,
        user_id,
    )
    return jsonify(updated), 200


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    delete_user(user_id)
    return jsonify({"id": user_id}), 200
