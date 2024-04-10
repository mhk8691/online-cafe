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
    cur.execute(
        "SELECT * FROM Payments LIMIT ?   ",
        (limit,),
    )
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


def get_all_payment_filter(name, search, limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM Payments   WHERE {name} = ? LIMIT {limit}",
        (search,),
    )
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
    x = re.split(",", range)
    final_range = re.split("]", x[1])[0]
    get_filter = request.args.get("filter")
    payment = get_all_payment(int(final_range) + 1)
    response = jsonify(payment)
    if len(get_filter) > 2:
        name = re.split(r""":""", get_filter)
        name2 = re.split(r"""^{\"""", name[0])
        name2 = re.split(r"""\"$""", name2[1])
        regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

        response = jsonify(
            get_all_payment_filter(
                name2[0],
                regex_filter[1],
                int(final_range) + 1,
            ),
        )

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
