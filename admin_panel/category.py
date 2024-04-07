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
    x = re.split(",", range)
    final_range = re.split("]", x[1])[0]
    categories = get_all_category(int(final_range) + 1)
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
