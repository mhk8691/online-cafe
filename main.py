from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3
import connect_db
import user_acount

# Connect to the database
conn = sqlite3.connect("onlineShop.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
connection = conn.cursor()

app = connect_db.app
customer_information = user_acount.customer_information


# home page
@app.route("/home/", methods=["POST", "GET"])
def home():
    if len(customer_information) == 0:
        return redirect(url_for("login"))
    else:
        return render_template("pages/index.html")


if __name__ == "__main__":
    app.run(debug=True)
