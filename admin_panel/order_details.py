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


# Get all products
def get_all_order_details(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT *  FROM Order_Details  LIMIT {limit}")
    Order_Details = cur.fetchall()
    final_Order_Details = []
    for order_detail in Order_Details:
        cur.execute(
            f"SELECT name FROM Products  WHERE product_id = ? LIMIT {limit}",
            (order_detail[2],),
        )
        product_name = cur.fetchall()
        for product in product_name:
            cur.execute(
                f"SELECT Customers.username FROM Customers INNER JOIN Orders on Customers.customer_id = Orders.customer_id WHERE order_id = ? ",
                (order_detail[1],),
            )
            username = cur.fetchone()[0]
            final_Order_Details.append(
                {
                    "id": order_detail[0],
                    "order_id": order_detail[1],
                    "username": username,
                    "product_name": product[0],
                    "quantity": order_detail[3],
                    "unit_price": order_detail[4],
                }
            )
    conn.close()
    return final_Order_Details


def get_all_order_details_filter(name, search, limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT *,name  FROM Order_Details INNER JOIN Products ON Products.product_id =Order_Details.product_id WHERE {name} = ? LIMIT {limit} ",
        (search,),
    )
    Order_Details = cur.fetchall()
    final_Order_Details = []
    for order_detail in Order_Details:

        cur.execute(
            "SELECT Customers.username FROM Customers INNER JOIN Orders on Customers.customer_id = Orders.customer_id WHERE order_id = ?",
            (order_detail[1],),
        )
        username = cur.fetchone()
        for name in username:
            final_Order_Details.append(
                {
                    "id": order_detail[0],
                    "order_id": order_detail[1],
                    "username": name,
                    "product_name": order_detail[6],
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
    x = re.split(",", range)
    final_range = re.split("]", x[1])[0]
    get_filter = request.args.get("filter")
    final_range2 = int(final_range) + 1
    print(final_range2)
    order_details = get_all_order_details(final_range2)
    response = jsonify(order_details)
    if len(get_filter) > 2:
        name = re.split(r""":""", get_filter)
        name2 = re.split(r"""^{\"""", name[0])
        name2 = re.split(r"""\"$""", name2[1])
        regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

        response = jsonify(
            get_all_order_details_filter(
                name2[0],
                regex_filter[1],
                int(final_range) + 1,
            ),
        )

    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(order_details)

    return response
