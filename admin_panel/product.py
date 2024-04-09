from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re
from fileinput import filename


app = connect_db.app


cors = CORS(app)
UPLOAD_FOLDER = "static/img/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


# Get a product by ID
def get_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM Products INNER JOIN Categories ON Categories.category_id =Products.categories_id  WHERE product_id = ?",
        (product_id,),
    )

    product = cur.fetchone()

    # picture_base64 = base64.b64encode(product[4]).decode("utf-8")

    cur.execute(
        "SELECT Categories.name FROM Products INNER JOIN Categories ON Products.categories_id = Categories.category_id WHERE category_id = ?",
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
def update_product(name, description, price, product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE products SET name = ?,description = ?, price = ? WHERE product_id = ?",
        (name, description, price, product_id),
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


import os
import requests

# CRUD routes
@app.route("/product/", methods=["GET"])
def list_product():
    range = request.args.get("range")
    x = re.split(",", range)
    final_range = re.split("]", x[1])[0]
    products = get_all_product(int(final_range) + 1)
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
    image = request.json["pictures"]
    # url = image["src"] + "/" + image["title"]
    print(image)
    product_id = create_product(name, description, price, categories_id, "image")
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
    # categories_id = request.json["categories_id"]
    # category_name = request.json["categories_name"]

    updated = update_product(name, description, price, product_id)
    return jsonify(updated), 200


@app.route("/product/<int:product_id>", methods=["DELETE"])
def delete_product_by_id(product_id):
    delete_product(product_id)
    return jsonify({"id": product_id}), 200
