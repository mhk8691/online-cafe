from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re
import admin_panel.user_login as user_login

user_information = user_login.user_information
app = connect_db.app


cors = CORS(app)
app.config["UPLOAD_FOLDER"] = "static/img/"


def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn

time = datetime.today().strftime("%Y-%m-%d")


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
def get_all_order(limit,sort):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"""SELECT order_id,Customers.username,order_date,total_amount,status
        FROM Orders
        INNER JOIN Customers
         ON Customers.customer_id = Orders.customer_id
        order by {sort}
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


# Get all order
def get_all_order_filter(name, search, limit,sort):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"""SELECT order_id,Customers.username,order_date,total_amount,status
        FROM Orders
        INNER JOIN Customers
         ON Customers.customer_id = Orders.customer_id
            WHERE {name} = ? order by {sort} LIMIT {limit}
         """,
        (search,),
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
    role = user_information[4]
    
    if role == "Admin" or role == "Super Admin":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Orders SET status = ? WHERE order_id = ?",
            (status, order_id),
        )

        conn.commit()
        conn.close()
        return get_order(order_id)




@app.route("/orders/", methods=["GET"])
def list_order():
    if len(user_information) !=0:
        range = request.args.get("range")
        sort = request.args.get("sort")
        get_filter = request.args.get("filter")

        final_range = json.loads(range)
        final_sort = json.loads(sort)
        
        if final_sort[0] == "id":
            final_sort[0] = "order_id"
        if final_sort[0] == "customer_name":
            final_sort[0] = "customer_id"
            
        final_sort2 = final_sort[0] + " " + final_sort[1]
        
        order = get_all_order(int(final_range[1]) + 1,final_sort2)
        response = jsonify(order)
        if len(get_filter) > 2:
            name = re.split(r""":""", get_filter)
            name2 = re.split(r"""^{\"""", name[0])
            name2 = re.split(r"""\"$""", name2[1])
            regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

            response = jsonify(
                get_all_order_filter(
                    name2[0],
                    regex_filter[1],
                    int(final_range[1]) + 1,
                    final_sort2
                ),
            )

        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
        response.headers["Content-Range"] = len(order)

        return response


@app.route("/orders", methods=["POST"])
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order_by_id(order_id):
    if len(user_information) !=0:
        order = get_order(order_id)
        if order is None:
            return "", 404
        return jsonify(order), 200


@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order_by_id(order_id):
    if len(user_information) !=0:
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
        elif status == "Cancel":
            statusToPershian = "لغو"
        message = f"سفارش شما در حالت {statusToPershian} قرار گرفت"

        notification(
            ci,
            message,
            time,
            "Unread",
        )
        name = get_order(order_id)
        
        user_ip = request.remote_addr
        action = f"Update Order name :{name["username"]} status :{status}"
        admin_log(3, action, time, user_ip)
        
        updated = update_order(
            status,
            order_id,
        )
        return jsonify(updated), 200


