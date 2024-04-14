import base64
from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re
from fileinput import filename
import os
import admin_panel.user_login as user_login

app = connect_db.app


user_information = user_login.user_information
cors = CORS(app)
UPLOAD_FOLDER = "static/img/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


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


time = datetime.today().strftime("%Y-%m-%d")


def get_data_from_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Categories")  # تغییر نام جدول به "Categories"
    data = cursor.fetchall()
    conn.close()
    # تبدیل داده‌ها به یک لیست از دیکشنری‌ها
    data_json = []
    for row in data:
        data_json.append(
            {
                "category_id": row[0],
                "category_name": row[1],
            }
        )
    return {"category": data_json}


def save_data_to_json(data):
    save_path = os.path.join(os.getcwd(), "shop-admin", "src", "category.json")
    if os.path.exists(save_path):
        os.remove(save_path)
    with open(save_path, "w") as f:
        json.dump(data, f, indent=4)


def save_data_route():
    data = get_data_from_database()
    save_data_to_json(data)
    return jsonify({"message": "Data saved to JSON file successfully!"})


# Get a product by ID
def get_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM Products   WHERE product_id = ?",
        (product_id,),
    )

    product = cur.fetchone()

    # picture_base64 = base64.b64encode(product[4]).decode("utf-8")

    cur.execute(
        "SELECT Categories.category_name FROM Products INNER JOIN Categories ON Products.categories_id = Categories.category_id WHERE category_id = ?",
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
        "category_name": category_name,
        "categories_id": product[5],
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
        picture_base64 = base64.b64encode(product[4]).decode("utf-8")
        cur.execute(
            "SELECT Categories.category_name FROM Categories WHERE category_id = ?",
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
                    "picture": picture_base64,
                    "category_name": name2,
                }
            )
    conn.close()
    return final_products


def get_all_product_filter(name, search, limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM Products WHERE {name} = ? LIMIT {limit}",
        (search,),
    )
    products = cur.fetchall()
    final_products = []
    for product in products:
        # picture_base64 = base64.b64encode(product[4]).decode("utf-8")
        cur.execute(
            "SELECT Categories.category_name FROM Categories WHERE category_id = ?",
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
                    "category_name": name2,
                }
            )
    conn.close()
    return final_products


# Create a new product
def create_product(name, description, price, categories_id, picture):
    role = user_information[4]

    if role == "Admin" or role == "Super Admin":
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
def update_product(name, description, price, categories_id, product_id):
    role = user_information[4]

    if role == "Admin" or role == "Super Admin":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE products SET name = ?,description = ?, price = ? , categories_id= ? WHERE product_id = ?",
            (
                name,
                description,
                price,
                categories_id,
                product_id,
            ),
        )
        conn.commit()
        conn.close()
        return get_product(product_id)


# Delete a product
def delete_product(product_id):
    role = user_information[4]

    if role == "Admin" or role == "Super Admin":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        cur.execute("DELETE FROM cart WHERE product_id = ?", (product_id,))
        conn.commit()
        conn.close()


# CRUD routes
@app.route("/product/", methods=["GET"])
def list_product():
    if len(user_information) != 0:
        range = request.args.get("range")
        x = re.split(",", range)
        final_range = re.split("]", x[1])[0]
        get_filter = request.args.get("filter")
        product = get_all_product(int(final_range) + 1)
        response = jsonify(product)
        if len(get_filter) > 2:
            name = re.split(r""":""", get_filter)
            name2 = re.split(r"""^{\"""", name[0])
            name2 = re.split(r"""\"$""", name2[1])
            regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

            response = jsonify(
                get_all_product_filter(
                    name2[0],
                    regex_filter[1],
                    int(final_range) + 1,
                ),
            )

        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
        response.headers["Content-Range"] = len(product)

        return response


@app.route("/product", methods=["POST"])
def add_product():
    if len(user_information) != 0:
        name = request.json["name"]
        description = request.json["description"]
        price = request.json["price"]
        categories_id = request.json["categories_id"]
        
        user_ip = request.remote_addr

        action = f"Add product: {name}"
        admin_log(3, action, time, user_ip)
        product_id = create_product(name, description, price, categories_id, "image")
        return (
            jsonify(
                get_product(product_id),
            ),
            201,
        )


@app.route("/product/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    if len(user_information) != 0:
        product = get_product(product_id)
        if product is None:
            return "", 404
        return jsonify(product), 200


def get_category_id(categories_name):
    if len(user_information) != 0:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT category_id FROM Categories  WHERE Categories.name = ?",
            (categories_name,),
        )
        category_id = cur.fetchone()
        for cat in category_id:
            final_category_id = cat
        return final_category_id


@app.route("/product/<int:product_id>", methods=["PUT"])
def update_product_by_id(product_id):
    if len(user_information) != 0:
        name = request.json["name"]
        description = request.json["description"]
        price = request.json["price"]
        categories_id = request.json["categories_id"]
        user_ip = request.remote_addr

        action = f"Update product: {name}"
        admin_log(3, action, time, user_ip)
        updated = update_product(name, description, price, categories_id, product_id)
        return jsonify(updated), 200


def get_name(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name from Products where product_id = ?", (product_id,))
    name = cur.fetchone()

    for name2 in name:
        final_name = name2
    return final_name


@app.route("/product/<int:product_id>", methods=["DELETE"])
def delete_product_by_id(product_id):
    if len(user_information) != 0:
        user_ip = request.remote_addr
        name = get_name(product_id)
        action = f"Delete product: {name}"
        admin_log(3, action, time, user_ip)
        delete_product(product_id)
        return jsonify({"id": product_id}), 200
