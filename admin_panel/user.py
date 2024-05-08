from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re
import os
import admin_panel.user_login as user_login

user_information = user_login.user_information
app = connect_db.app


cors = CORS(app)
app.config["UPLOAD_FOLDER"] = "static/img/"


def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


# Get a user by ID
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))

    user = cur.fetchone()

    final_user = {
        "id": user[0],
        "username": user[1],
        "password": user[2],
        "email": user[3],
        "role": user[4],
    }

    conn.close()
    return final_user


# Get all user
def get_all_user(limit, sort):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM Users WHERE role != ?  order by {sort}  LIMIT {limit}",
        ("Super Admin",),
    )
    users = cur.fetchall()
    final_users = []
    for user in users:
        final_users.append(
            {
                "id": user[0],
                "username": user[1],
                "password": user[2],
                "email": user[3],
                "role": user[4],
            }
        )
    conn.close()
    return final_users


# Get all user
def get_all_user_filter(name, search, limit, sort):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM Users WHERE {name} = ? AND role != ?  order by {sort} LIMIT {limit}",
        (
            search,
            "Super Admin",
        ),
    )
    users = cur.fetchall()
    final_users = []
    for user in users:
        final_users.append(
            {
                "id": user[0],
                "username": user[1],
                "password": user[2],
                "email": user[3],
                "role": user[4],
            }
        )
    conn.close()
    return final_users


# Create a new user
def create_user(
    username,
    password,
    email,
    role,
):
    role2 = user_information[4]

    if role2 == "Super Admin":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Users (username,password, email,role) VALUES (?, ?, ?,?)",
            (
                username,
                password,
                email,
                role,
            ),
        )
        conn.commit()
        user_id = cur.lastrowid
        conn.close()
        return user_id


# Update a user
def update_user(
    username,
    password,
    email,
    role,
    user_id,
):
    role2 = user_information[4]

    if role2 == "Super Admin":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Users SET username = ?,password = ?, email = ?, role = ? WHERE user_id = ?",
            (
                username,
                password,
                email,
                role,
                user_id,
            ),
        )
        conn.commit()
        conn.close()
        return get_user(user_id)


# Delete a user
def delete_user(user_id):
    role2 = user_information[4]

    if role2 == "Super Admin":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()


# CRUD routes
@app.route("/user/", methods=["GET"])
def list_user():
    if len(user_information) != 0:
        range = request.args.get("range")
        sort = request.args.get("sort")
        get_filter = request.args.get("filter")

        final_range = json.loads(range)
        final_sort = json.loads(sort)

        if final_sort[0] == "id":
            final_sort[0] = "user_id"

        final_sort2 = final_sort[0] + " " + final_sort[1]
        user = get_all_user(int(final_range[1]) + 1, final_sort2)
        response = jsonify(user)
        if len(get_filter) > 2:
            name = re.split(r""":""", get_filter)
            name2 = re.split(r"""^{\"""", name[0])
            name2 = re.split(r"""\"$""", name2[1])
            regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

            response = jsonify(
                get_all_user_filter(
                    name2[0], regex_filter[1], int(final_range[1]) + 1, final_sort2
                ),
            )

        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
        response.headers["Content-Range"] = len(user)

        return response


@app.route("/user", methods=["POST"])
def add_user():
    if len(user_information) != 0:
        username = request.json["username"]
        password = request.json["password"]
        email = request.json["email"]
        role = request.json["role"]

        userlist = create_user(
            username,
            password,
            email,
            role,
        )

        return jsonify(get_user(userlist)), 201


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    if len(user_information) != 0:
        user = get_user(user_id)
        if user is None:
            return "", 404
        return jsonify(user), 200


@app.route("/user/<int:user_id>", methods=["PUT"])
def update_user_by_id(user_id):
    if len(user_information) != 0:
        username = request.json["username"]
        password = request.json["password"]
        email = request.json["email"]
        role = request.json["role"]

        updated = update_user(
            username,
            password,
            email,
            role,
            user_id,
        )

        return jsonify(updated), 200


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    if len(user_information) != 0:
        delete_user(user_id)

        return jsonify({"id": user_id}), 200
