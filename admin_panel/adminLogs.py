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


def get_log(log_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT *,username FROM Admin_Logs INNER JOIN Users ON Admin_Logs.user_id = Users.user_id WHERE log_id = ?",
        (log_id,),
    )

    logs = cur.fetchone()

    final_logs = {
        "id": logs[0],
        "username": logs[6],
        "action": logs[2],
        "action_date": logs[3],
        "ip_address": logs[4],
        # "picture": category[5],
    }

    conn.close()
    return final_logs


# Get all products
def get_all_log(limit,sort):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT *,username FROM Admin_Logs INNER JOIN Users ON Admin_Logs.user_id = Users.user_id order by {sort} LIMIT ?   ",
        (limit,),
    )
    logs = cur.fetchall()
    final_logs = []
    for log in logs:
        final_logs.append(
            {
                "id": log[0],
                "username": log[6],
                "action": log[2],
                "action_date": log[3],
                "ip_address": log[4],
                # "picture": category[5],
            }
        )
    conn.close()
    return final_logs


# Get all products
def get_all_log_filter(name, search, limit,sort):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT *,username FROM Admin_Logs INNER JOIN Users ON Admin_Logs.user_id = Users.user_id  WHERE {name} = ? order by {sort} LIMIT {limit}",
        (search,),
    )
    logs = cur.fetchall()
    final_logs = []
    for log in logs:
        final_logs.append(
            {
                "id": log[0],
                "username": log[6],
                "action": log[2],
                "action_date": log[3],
                "ip_address": log[4],
                # "picture": category[5],
            }
        )
    conn.close()
    return final_logs


@app.route("/admin_logs/", methods=["GET"])
def list_log():
    if len(user_information) !=0:
        range = request.args.get("range")
        sort = request.args.get("sort")
        get_filter = request.args.get("filter")

        final_range = json.loads(range)
        final_sort = json.loads(sort)

        if final_sort[0] == "id":
            final_sort[0] = "log_id"
        if final_sort[0] == "username":
            final_sort[0] = "user_id"

        final_sort2 = final_sort[0] + " " + final_sort[1]
        log = get_all_log(int(final_range[1]) + 1, final_sort2)
        response = jsonify(log)
        if len(get_filter) > 2:
            name = re.split(r""":""", get_filter)
            name2 = re.split(r"""^{\"""", name[0])
            name2 = re.split(r"""\"$""", name2[1])
            regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

            response = jsonify(
                get_all_log_filter(
                    name2[0], regex_filter[1], int(final_range[1]) + 1, final_sort2
                ),
            )

        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
        response.headers["Content-Range"] = len(log)

        return response


@app.route("/admin_logs", methods=["POST"])
@app.route("/admin_logs/<int:log_id>", methods=["GET"])
def get_log_by_id(log_id):
    if len(user_information) !=0:
        log = get_log(log_id)
        if log is None:
            return "", 404
        return jsonify(log), 200
