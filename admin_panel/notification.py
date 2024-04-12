from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re

app = connect_db.app

time = datetime.today().strftime("%Y-%m-%d")


def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


text = "Admin"


# Create a new customer
def create_notification(customer_id, message, created_at, status):
    if text == "Admin" or text == "Super Admin":

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Notifications (customer_id,message,created_at,status) VALUES (?, ?,?,?)",
            (customer_id, message, created_at, status),
        )
        conn.commit()
        notification = cur.lastrowid
        conn.close()
        return notification


# Get a customer by ID
def get_notification(notificationـid):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM Notifications WHERE notificationـid = ?", (notificationـid,)
    )
    notif = cur.fetchone()
    final_notif = {
        "id": notif[0],
        "customer_id": notif[1],
        "message": notif[2],
        "created_at": notif[3],
        "status": notif[4],
    }
    conn.close()
    return final_notif


# Get all customers
def get_all_notification(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM Notifications LIMIT ?",
        (str(limit),),
    )
    notif = cur.fetchall()
    final_notifications = []
    for notif2 in notif:
        final_notifications.append(
            {
                "id": notif2[0],
                "customer_id": notif2[1],
                "message": notif2[2],
                "created_at": notif2[3],
                "status": notif2[4],
            }
        )
    conn.close()
    return final_notifications


def get_all_notification_filter(name, search, limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM Notifications LIMIT ?",
        (str(limit),),
    )
    cur.execute(
        f"SELECT * FROM Notifications   WHERE {name} = ? LIMIT {limit}",
        (search,),
    )
    notif = cur.fetchall()
    final_notifications = []
    for notif2 in notif:
        final_notifications.append(
            {
                "id": notif2[0],
                "customer_id": notif2[1],
                "message": notif2[2],
                "created_at": notif2[3],
                "status": notif2[4],
            }
        )
    conn.close()
    return final_notifications


@app.route("/Notification/<int:notification_id>", methods=["GET"])
def get_notification_by_id(notification_id):
    feedback = get_notification(notification_id)
    if feedback is None:
        return "", 404
    return jsonify(feedback), 200


@app.route("/Notification/", methods=["GET"])
def list_notification():
    range = request.args.get("range")
    x = re.split(",", range)
    final_range = re.split("]", x[1])[0]
    get_filter = request.args.get("filter")
    notif = get_all_notification(int(final_range) + 1)
    response = jsonify(notif)
    if len(get_filter) > 2:
        name = re.split(r""":""", get_filter)
        name2 = re.split(r"""^{\"""", name[0])
        name2 = re.split(r"""\"$""", name2[1])
        regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

        response = jsonify(
            get_all_notification_filter(
                name2[0],
                regex_filter[1],
                int(final_range) + 1,
            ),
        )

    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(notif)

    return response


def get_id(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT customer_id FROM Customers WHERE username = ?", (username,))
    id = cur.fetchone()[0]
    return id


@app.route("/Notification", methods=["POST"])
def add_notification():
    username = request.json["username"]
    message = request.json["message"]
    id = get_id(username)
    notificationـid = create_notification(id, message, time, "Unread")
    return jsonify(get_notification(notificationـid)), 201


# Delete a customer
def delete_notification(notificationـid):
    if text == "Admin" or text == "Super Admin":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM Notifications WHERE notificationـid = ?", (notificationـid,)
        )

        conn.commit()
        conn.close()


@app.route("/Notification/<int:notification_id>", methods=["DELETE"])
def delete_notification_by_id(notification_id):

    delete_notification(notification_id)
    return jsonify({"id": notification_id}), 200
