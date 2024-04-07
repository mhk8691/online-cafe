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
    x = re.split(",", range)
    final_range = re.split("]", x[1])[0]
    shippings = get_all_shipping(int(final_range) + 1)
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
