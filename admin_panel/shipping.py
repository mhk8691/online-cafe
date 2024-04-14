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
def get_all_shipping(limit,sort):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM Shipping_Addresses order by {sort} LIMIT " + str(limit))
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


def get_all_shipping_filter(name, search, limit,sort):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM Shipping_Addresses WHERE {name} = ?  order by {sort}  LIMIT {limit}",
        (search,),
    )
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
    role = user_information[4]

    if role == "Admin" or role == "Super Admin":
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
    role = user_information[4]

    if role == "Admin" or role == "Super Admin":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Shipping_Addresses WHERE address_id = ?", (address_id,))
        conn.commit()
        conn.close()


# CRUD routes
@app.route("/shipping/", methods=["GET"])
def list_shipping():
    if len(user_information) !=0:
        range = request.args.get("range")
        sort = request.args.get("sort")
        get_filter = request.args.get("filter")

        final_range = json.loads(range)
        final_sort = json.loads(sort)
        
        if final_sort[0] == "id":
            final_sort[0] = "address_id"
        if final_sort[0] == "customer_name":
            final_sort[0] = "customer_id"
        final_sort2 = final_sort[0] + " " + final_sort[1]
        
        
        shipping = get_all_shipping(int(final_range[1]) + 1, final_sort2)
        response = jsonify(shipping)
        if len(get_filter) > 2:
            name = re.split(r""":""", get_filter)
            name2 = re.split(r"""^{\"""", name[0])
            name2 = re.split(r"""\"$""", name2[1])
            regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

            response = jsonify(
                get_all_shipping_filter(
                    name2[0], regex_filter[1], int(final_range[1]) + 1, final_sort2
                ),
            )

        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
        response.headers["Content-Range"] = len(shipping)

        return response


@app.route("/shipping", methods=["POST"])


@app.route("/shipping/<int:address_id>", methods=["GET"])
def get_shipping_by_id(address_id):
    if len(user_information) != 0:
        shipping = get_shipping(address_id)
        if shipping is None:
            return "", 404
        return jsonify(shipping), 200


@app.route("/shipping/<int:address_id>", methods=["PUT"])
def update_shipping_by_id(address_id):
    if len(user_information) != 0:
        recipient_name = request.json["recipient_name"]
        address_line1 = request.json["address_line1"]
        address_line2 = request.json["address_line2"]
        city = request.json["city"]
        state = request.json["state"]
        postal_code = request.json["postal_code"]
        country = request.json["country"]
        user_ip = request.remote_addr
        action = f"Update shipping: {recipient_name}"
        admin_log(3, action, time, user_ip)
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


def get_name(shipping_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT recipient_name from Shipping_Addresses where address_id = ?",
        (shipping_id,),
    )
    username = cur.fetchone()

    for user in username:
        final_username = user
    return final_username


@app.route("/shipping/<int:address_id>", methods=["DELETE"])
def delete_shipping_by_id(address_id):
    if len(user_information) !=0:
        user_ip = request.remote_addr
        name = get_name(address_id)
        action = f"Delete shipping: {name}"
        admin_log(3, action, time, user_ip)
        delete_shipping(address_id)
        return jsonify({"id": address_id}), 200
