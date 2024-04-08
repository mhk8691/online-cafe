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


# Get all feedback
def get_all_feedback(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Feedback LIMIT ?", (str(limit),))
    feedbacks = cur.fetchall()
    final_feedback = []
    for feedback in feedbacks:
        cur.execute(
            "SELECT Customers.username FROM Customers WHERE customer_id = ?",
            (feedback[1],),
        )
        username = cur.fetchone()
        for username2 in username:

            final_feedback.append(
                {
                    "id": feedback[0],
                    "customer_name": username2,
                    "order_id": feedback[2],
                    "rating": feedback[3],
                    "comment": feedback[4],
                    "feedback_date": feedback[5],
                }
            )
    conn.close()
    return final_feedback


@app.route("/feedback", methods=["POST"])
@app.route("/feedback/", methods=["GET"])
def list_feedback():
    range = request.args.get("range")
    sort = request.args.get("sort")
    x = re.split(",", range)
    final_range = re.split("]", x[1])[0]
    sort = re.split(",",sort)
    z = re.split("^\[",sort[1])
    print(z[0])

    payment = get_all_feedback(int(final_range) + 1)
    response = jsonify(payment)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(payment)
    return response
