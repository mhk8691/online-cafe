from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re

app = connect_db.app
import admin_panel.user_login as user_login

user_information = user_login.user_information

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
def get_all_payment(limit,sort):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM Payments order by {sort} LIMIT ?   ",
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


def get_all_payment_filter(name, search, limit,sort):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM Payments   WHERE {name} = ? order by {sort} LIMIT {limit}",
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
    if len(user_information) !=0:
        range = request.args.get("range")
        sort = request.args.get("sort")
        get_filter = request.args.get("filter")

        final_range = json.loads(range)
        final_sort = json.loads(sort)

        if final_sort[0] == "id":
            final_sort[0] = "payment_id"
        

        final_sort2 = final_sort[0] + " " + final_sort[1]

        payment = get_all_payment(int(final_range[1]) + 1, final_sort2)
        response = jsonify(payment)
        if len(get_filter) > 2:
            name = re.split(r""":""", get_filter)
            name2 = re.split(r"""^{\"""", name[0])
            name2 = re.split(r"""\"$""", name2[1])
            regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

            response = jsonify(
                get_all_payment_filter(
                    name2[0], regex_filter[1], int(final_range[1]) + 1, final_sort2
                ),
            )

        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
        response.headers["Content-Range"] = len(payment)

        return response


@app.route("/payment", methods=["POST"])
@app.route("/payment/<int:order_id>", methods=["GET"])
def get_payment_by_id(order_id):
    if len(user_information) !=0:
        payment = get_payment(order_id)
        if payment is None:
            return "", 404
        return jsonify(payment), 200
