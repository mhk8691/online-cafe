from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3
import connect_db as connect_db
import user_acount as user_acount
import admin as admin
import base64
import product as product

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
        connection.execute("select * from Categories  ")
        categories = connection.fetchall()
        list = []

        for category in categories:
            picture_base64 = base64.b64encode(category[5]).decode("utf-8")
            list.append(
                {
                    "category_id": category[0],
                    "name": category[1],
                    "description": category[2],
                    "picture": picture_base64,
                }
            )

        return render_template("pages/index.html", list=list, len=len(list))


@app.route("/checkout/", methods=["POST", "GET"])
def checkout():
    if request.method == "POST":
        recipient_name = request.form["recipient_name"]
        address_line1 = request.form["address_line1"]
        address_line2 = request.form["address_line2"]
        city = request.form["city"]
        state = request.form["state"]
        postal_code = request.form["postal_code"]
        country = request.form["country"]
        connection.execute(
            """ INSERT INTO Shipping_Addresses(customer_id,recipient_name,address_line1,address_line2,city,state,postal_code,country)
VALUES (?,?,?,?,?,?,?,?)  """,
            (
                customer_information[0],
                recipient_name,
                address_line1,
                address_line2,
                city,
                state,
                postal_code,
                country,
            ),
        )
        conn.commit()

    return render_template("pages/checkout.html")


if __name__ == "__main__":
    app.run(debug=True)
