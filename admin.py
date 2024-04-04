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

    cur.execute(
        "SELECT Categories.name FROM Categories WHERE category_id = ?",
        (product[5],),
    )
    name = cur.fetchone()
    for name2 in name:
        category_name = name2
    final_product = {
        "id": product[0],
        "name": product[1],
        "description": product[2],
        "price": product[3],
        "categories_name": category_name,
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
        cur.execute(
            "SELECT Categories.name FROM Categories WHERE category_id = ?",
            (product[5],),
        )
        name = cur.fetchone()
        for name2 in name:

            final_products.append(
                {
                    "id": product[0],
                    "name": product[1],
                    "description": product[2],
                    "price": product[3],
                    # "picture": picture_base64,
                    "categories_name": name2,
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
def update_product(product_id, name, description, price, categories_id, category_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE products SET name = ?,description = ?, price = ?,categories_id = ? WHERE product_id = ? AND category_name = ?",
        (name, description, price, categories_id, product_id, category_name),
    )
    conn.commit()
    conn.close()
    return get_product(product_id)


# Delete a product
def delete_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    cur.execute("DELETE FROM cart WHERE product_id = ?", (product_id,))
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


# @app.route("/product/create/")
# def test():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT category_id,name FROM Categories")
#     category_list = cur.fetchall()
#     category_list2 = []
#     for cat in category_list:
#         category_list2.append({"id": cat[0], "name": cat[1]})

#     return category_list2


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
    category_name = request.json["categories_name"]

    updated = update_product(
        product_id, name, description, price, categories_id, category_name
    )
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
    cur.execute("DELETE FROM Products WHERE categories_id = ?", (category_id,))
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
    cur.execute(
        "SELECT Customers.username FROM Customers WHERE customer_id = ?", (shipping[1],)
    )
    username = cur.fetchone()
    for username2 in username:

        final_shipping = {
            "id": shipping[0],
            "customer_name": username2,
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
        cur.execute(
            "SELECT Customers.username FROM Customers WHERE customer_id = ?",
            (shipping[1],),
        )
        username = cur.fetchone()
        for username2 in username:

            final_shipping.append(
                {
                    "id": shipping[0],
                    "customer_name": username2,
                    "recipient_name": shipping[2],
                    "address_line1": shipping[3],
                    "address_line2": shipping[4],
                    "city": shipping[5],
                    "state": shipping[6],
                    "postal_code": shipping[7],
                    "country": shipping[8],
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
        """UPDATE 
        Shipping_Addresses SET 
        recipient_name = ?, address_line1 = ?, address_line2 = ?, city = ?, state = ?, postal_code = ?, country = ?
        WHERE address_id = ?""",
        (
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
    recipient_name = request.json["recipient_name"]
    address_line1 = request.json["address_line1"]
    address_line2 = request.json["address_line2"]
    city = request.json["city"]
    state = request.json["state"]
    postal_code = request.json["postal_code"]
    country = request.json["country"]

    updated = update_shipping(
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
        "id": user[0],
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
                "id": user[0],
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


# -------------------------- order -----------------------


# Get a user by ID
def get_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT order_id,order_date,Customers.username,total_amount,status FROM Orders INNER JOIN Customers
        ON Customers.customer_id = Orders.customer_id  WHERE order_id = ?""",
        (order_id,),
    )

    order = cur.fetchone()

    final_order = {
        "id": order[0],
        "username": order[1],
        "order_date": order[2],
        "total_amount": order[3],
        "status": order[4],
    }

    conn.close()
    return final_order


# Get all order
def get_all_order(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT 
        order_id,Customers.username,order_date,total_amount,status
        FROM Orders
        INNER JOIN Customers
        ON Customers.customer_id = Orders.customer_id 
        
        LIMIT """
        + str(limit)
    )
    orders = cur.fetchall()
    final_orders = []
    for order in orders:
        cur.execute(
            """SELECT SUM(Order_Details.quantity)
            FROM Order_Details
            INNER JOIN Orders
            ON Orders.order_id = Order_Details.order_id
            WHERE Orders.order_id = ?
            """,
            (order[0],),
        )
        test = cur.fetchone()
        for t in test:

            final_orders.append(
                {
                    "id": order[0],
                    "username": order[1],
                    "order_date": order[2],
                    "total_amount": order[3],
                    "status": order[4],
                    "quantity": t,
                }
            )
    conn.close()
    return final_orders


# Update a user
def update_order(order_date, total_amount, status, order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Orders SET order_date = ?,total_amount = ?, status = ? WHERE order_id = ?",
        (order_date, total_amount, status, order_id),
    )
    conn.commit()
    conn.close()
    return get_order(order_id)


# Delete a user
def delete_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Orders WHERE order_id = ?", (order_id,))
    cur.execute(
        "DELETE FROM Order_Details WHERE Order_Details.order_id = ?", (order_id,)
    )
    cur.execute("DELETE FROM Payments WHERE Payments.order_id = ?", (order_id,))
    conn.commit()
    conn.close()


@app.route("/orders/", methods=["GET"])
def list_order():
    range = request.args.get("range")
    orders = get_all_order(int(range[3]) + 1)
    response = jsonify(orders)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(orders)
    return response


@app.route("/orders", methods=["POST"])
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order_by_id(order_id):
    order = get_order(order_id)
    if order is None:
        return "", 404
    return jsonify(order), 200


@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order_by_id(order_id):
    order_date = request.json["order_date"]
    total_amount = request.json["total_amount"]
    status = request.json["status"]

    updated = update_order(order_date, total_amount, status, order_id)
    return jsonify(updated), 200


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order_by_id(order_id):
    delete_order(order_id)
    return jsonify({"id": order_id}), 200


# -------------------------- order end -----------------------


# ------------------------------- payment start ------------------


# Get a product by ID
def get_payment(payment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Payments WHERE payment_id = ?", (payment_id,))

    payment = cur.fetchone()

    final_paymnet = {
        "id": payment[0],
        "order_id": payment[1],
        "payment_method": payment[2],
        "amount": payment[3],
        "payment_date": payment[4],
        # "picture": category[5],
    }

    conn.close()
    return final_paymnet


# Get all products
def get_all_payment(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Payments LIMIT " + str(limit))
    payments = cur.fetchall()
    final_payments = []
    for payment in payments:
        final_payments.append(
            {
                "id": payment[0],
                "order_id": payment[1],
                "payment_method": payment[2],
                "amount": payment[3],
                "payment_date": payment[4],
                # "picture": category[5],
            }
        )
    conn.close()
    return final_payments


@app.route("/payment/", methods=["GET"])
def list_payment():
    range = request.args.get("range")
    payment = get_all_payment(int(range[3]) + 1)
    response = jsonify(payment)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(payment)
    return response


@app.route("/payment", methods=["POST"])
@app.route("/payment/<int:order_id>", methods=["GET"])
def get_payment_by_id(order_id):
    payment = get_payment(order_id)
    if payment is None:
        return "", 404
    return jsonify(payment), 200


# .......................order details..........................


# Get all products
def get_all_order_details(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT *  FROM Order_Details LIMIT " + str(limit))
    Order_Details = cur.fetchall()
    final_Order_Details = []
    for order_detail in Order_Details:
        cur.execute(
            "SELECT name FROM Products  WHERE product_id = ?",
            (order_detail[2],),
        )
        product_name = cur.fetchall()
        for product in product_name:

            final_Order_Details.append(
                {
                    "id": order_detail[0],
                    "order_id": order_detail[1],
                    "product_name": product[0],
                    "quantity": order_detail[3],
                    "unit_price": order_detail[4],
                }
            )
    conn.close()
    return final_Order_Details


@app.route("/Order_Details", methods=["POST"])
@app.route("/Order_Details/", methods=["GET"])
def list_order_details():
    range = request.args.get("range")
    details = get_all_order_details(int(range[3]) + 1)
    response = jsonify(details)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(details)
    return response

# .......................order details end..........................
