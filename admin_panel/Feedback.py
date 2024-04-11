from flask import Flask, request, jsonify, json
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import re

app = connect_db.app


cors = CORS(app)
app.config["UPLOAD_FOLDER"] = "static/img/"

feedback_id2 = None


def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


# Get a user by ID
def get_feedback(feedback_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT feedback_id,Customers.username,order_id,rating,comment,feedback_date
        FROM Feedback
        INNER JOIN Customers
        ON Customers.customer_id = Feedback.customer_id
        
          WHERE feedback_id = ?""",
        (feedback_id,),
    )

    feedback = cur.fetchone()

    final_feedback = {
        "id": feedback[0],
        "customer_name": feedback[1],
        "order_id": feedback[2],
        "rating": feedback[3],
        "comment": feedback[4],
        "feedback_date": feedback[5],
    }
    conn.close()
    return final_feedback


# Get all feedback
def get_all_feedback(limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT *,username FROM Feedback INNER JOIN Customers ON Customers.customer_id = Feedback.customer_id   LIMIT ?",
        (str(limit),),
    )
    feedbacks = cur.fetchall()
    final_feedback = []
    for feedback in feedbacks:

        final_feedback.append(
            {
                "id": feedback[0],
                "customer_name": feedback[7],
                "order_id": feedback[2],
                "rating": feedback[3],
                "comment": feedback[4],
                "feedback_date": feedback[5],
            }
        )
    conn.close()
    return final_feedback




def get_all_feedback_filter(name, search, limit):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT *,username FROM Feedback INNER JOIN Customers ON Customers.customer_id = Feedback.customer_id  WHERE {name} = ? LIMIT {limit}",
        (search,),
    )
    feedbacks = cur.fetchall()
    final_feedback = []
    for feedback in feedbacks:
      

        final_feedback.append(
            {
                "id": feedback[0],
                "customer_name": feedback[7],
                "order_id": feedback[2],
                "rating": feedback[3],
                "comment": feedback[4],
                "feedback_date": feedback[5],
            }
        )
    conn.close()
    return final_feedback


@app.route("/feedback/<int:feedback_id>", methods=["GET"])
def get_feedback_by_id(feedback_id):
    feedback = get_feedback(feedback_id)
    feedback_id2 = feedback_id
    if feedback is None:
        return "", 404
    return jsonify(feedback), 200


@app.route("/feedback", methods=["POST"])
@app.route("/feedback/", methods=["GET"])
def list_feedback():
    range = request.args.get("range")
    x = re.split(",", range)
    final_range = re.split("]", x[1])[0]
    get_filter = request.args.get("filter")
    feedback = get_all_feedback(int(final_range) + 1)
    response = jsonify(feedback)
    if len(get_filter) > 2:
        name = re.split(r""":""", get_filter)
        name2 = re.split(r"""^{\"""", name[0])
        name2 = re.split(r"""\"$""", name2[1])
        regex_filter = re.split(rf'"{name2[0]}":"(.*?)"', get_filter)

        response = jsonify(
            get_all_feedback_filter(
                name2[0],
                regex_filter[1],
                int(final_range) + 1,
            ),
        )

    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = len(feedback)

    return response


# Update a user
def notification(customer_id, message, created_at, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Notifications(customer_id,message,created_at,status) VALUES (?,?,?,?)",
        (customer_id, message, created_at, status),
    )

    conn.commit()
    feed = cur.lastrowid

    conn.close()
    return feed


def customer_id(feedback_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT Feedback.customer_id
        FROM Feedback
        
          WHERE feedback_id = ?""",
        (feedback_id,),
    )
    customer_id = cur.fetchone()[0]
    return customer_id


print("hello")


@app.route("/feedback", methods=["POST"])
def add_feedback():
    # feedback_id = 2
    # customer_id = customer_id(8)
    message = request.json["message"]
    print(message)
    time = datetime.today().strftime("%Y-%m-%d")

    notif = notification(8, message, time, "Unread")
