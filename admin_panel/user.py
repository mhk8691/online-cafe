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
def get_all_user(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users LIMIT " + str(limit))
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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# CRUD routes
@app.route("/user/", methods=["GET"])
def list_user():
    range = request.args.get("range")
    x = re.split(",", range)
    final_range = re.split("]", x[1])[0]
    users = get_all_user(int(final_range) + 1)
    response = jsonify(users)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(users)
    return response


@app.route("/user", methods=["POST"])
def add_user():
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
    user = get_user(user_id)
    if user is None:
        return "", 404
    return jsonify(user), 200


@app.route("/user/<int:user_id>", methods=["PUT"])
def update_user_by_id(user_id):
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
    delete_user(user_id)
    return jsonify({"id": user_id}), 200
