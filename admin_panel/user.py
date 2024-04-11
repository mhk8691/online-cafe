from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re
import os

app = connect_db.app


cors = CORS(app)
app.config["UPLOAD_FOLDER"] = "static/img/"

text = "Super Admin"


def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_data_from_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    data = cursor.fetchall()
    conn.close()
    # تبدیل داده‌ها به یک لیست از دیکشنری‌ها

    data_json = [
        {
            "id": row[0],
            "username": row[1],
            "password": row[2],
            "email": row[3],
            "role": row[4],
        }
        for row in data
    ]
    return {"users": data_json}


def save_data_to_json(data):
    save_path = os.path.join(os.getcwd(), "shop-admin", "src", "users.json")
    os.remove(save_path)
    with open(save_path, "w") as f:
        json.dump(data, f, indent=4)


def save_data_route():
    data = get_data_from_database()
    save_data_to_json(data)
    print("hello")
    return jsonify({"message": "Data saved to JSON file successfully!"})


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


# Get all user
def get_all_user_filter(name, search, limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM Users WHERE {name} = ? LIMIT {limit}",
        (search,),
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
    if text == "Super Admin":
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
    if text == "Super Admin":
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
    if text == "Super Admin":
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
    get_filter = request.args.get("filter")
    user = get_all_user(int(final_range) + 1)
    response = jsonify(user)
    if len(get_filter) > 2:
        name = re.split(r""":""", get_filter)
        name2 = re.split(r"""^{\"""", name[0])
        name2 = re.split(r"""\"$""", name2[1])
        regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

        response = jsonify(
            get_all_user_filter(
                name2[0],
                regex_filter[1],
                int(final_range) + 1,
            ),
        )

    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(user)

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
    save_data_route()

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
    save_data_route()

    return jsonify(updated), 200


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    delete_user(user_id)
    save_data_route()

    return jsonify({"id": user_id}), 200
