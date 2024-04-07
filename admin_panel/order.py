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


# Get a user by ID
def get_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT order_id,Customers.username,order_date,total_amount,status
        FROM Orders
        INNER JOIN Customers
         ON Customers.customer_id = Orders.customer_id
          WHERE order_id = ?""",
        (order_id,),
    )

    order = cur.fetchone()
    cur.execute(
        "SELECT SUM(Order_Details.quantity) FROM Order_Details INNER JOIN Orders ON Order_Details.order_id =Orders.order_id  WHERE Order_Details.order_id = ?",
        (order[0],),
    )
    quantity = cur.fetchone()
    for q in quantity:

        final_order = {
            "id": order[0],
            "username": order[1],
            "order_date": order[2],
            "total_amount": order[3],
            "status": order[4],
            "quantity": q,
        }
    conn.close()
    return final_order


def customer_id(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT Orders.customer_id
        FROM Orders
        
          WHERE order_id = ?""",
        (order_id,),
    )
    customer_id = cur.fetchone()[0]
    return customer_id


# Get all order
def get_all_order(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT order_id,Customers.username,order_date,total_amount,status
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
        quantity = cur.fetchone()
        for q in quantity:

            final_orders.append(
                {
                    "id": order[0],
                    "username": order[1],
                    "order_date": order[2],
                    "total_amount": order[3],
                    "status": order[4],
                    "quantity": q,
                }
            )
    conn.close()
    return final_orders


def notification(
    customer_id,
    message,
    created_at,
    status_notification,
):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Notifications (customer_id,message, created_at,status) VALUES (?, ?, ?,?)",
        (
            customer_id,
            message,
            created_at,
            status_notification,
        ),
    )
    conn.commit()
    conn.close()


# Update a user
def update_order(
    status,
    order_id,
):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Orders SET status = ? WHERE order_id = ?",
        (status, order_id),
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
    x = re.split(",",range)
    final_range = re.split("]",x[1])[0]
    orders = get_all_order(int(final_range)+1)
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

    status = request.json["status"]
    ci = customer_id(order_id)
    time = datetime.today().strftime("%Y-%m-%d")
    statusToPershian = ""
    if status == "Send":
        statusToPershian = "ارسال"
    elif status == "Confirmation":
        statusToPershian = "تایید"
    elif status == "Delivery":
        statusToPershian = "تحویل"
    message = f"سفارش شما در حالت {statusToPershian} قرار گرفت"

    notification(
        ci,
        message,
        time,
        "Unread",
    )
    updated = update_order(
        status,
        order_id,
    )
    return jsonify(updated), 200


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order_by_id(order_id):
    delete_order(order_id)
    return jsonify({"id": order_id}), 200
