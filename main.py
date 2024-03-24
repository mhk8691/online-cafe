from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3
import connect_db as connect_db
import user_acount as user_acount
import admin as admin
import base64
import product as product
from datetime import datetime


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


def Totalprice():
    sql = """
        SELECT SUM(quantity * Products.price), SUM(quantity)
        FROM cart
        INNER JOIN Products ON cart.product_id = Products.product_id
        WHERE customer_id = ?
        """

    connection.execute(
        sql, (customer_information[0],)
    )  # Enclose customer_id in a tuple for a single parameter

    list_price = connection.fetchall()
    list_price2 = []
    for price in list_price:
        list_price2.append({"Totalprice": price[0], "quantity": price[1]})

    return list_price2


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
    list_price2 = Totalprice()
    connection.execute(
        """SELECT Products.product_id,Products.name,Products.description,Products.price,Products.picture,quantity
                from Products
                inner join cart
                on cart.product_id = Products.product_id
                where cart.customer_id = ?""",
        (customer_information[0],),
    )
    carts = connection.fetchall()

    product_list = []

    for cart in carts:

        product_list.append(
            {
                "product_id": cart[0],
                "name": cart[1],
                "description": cart[2],
                "price": cart[3],
                "picture": base64.b64encode(cart[4]).decode("utf-8"),
                "quantity": cart[5],
            }
        )
    return render_template(
        "pages/checkout.html", product_list=product_list, list_price2=list_price2
    )


show_cart = product.show_cart


@app.route("/end-payment/")
def end_payment():
    time = datetime.today().strftime("%Y-%m-%d")
    connection.execute(
        """
    SELECT SUM(quantity)
    FROM cart
    INNER JOIN Products ON cart.product_id = Products.product_id
    WHERE customer_id = ?
    """,
        (int(customer_information[0]),),
    )
    quantity = connection.fetchone()

    for q in quantity:
        quantity2 = q

    connection.execute(
        "INSERT INTO Orders (customer_id,order_date,total_amount,status) VALUES (?,?,?,?)",
        (int(customer_information[0]), time, quantity2, "test"),
    )

    product_list = []
    carts = show_cart()
    for cart in carts:

        product_list.append(
            {
                "product_id": cart[0],
                "name": cart[1],
                "description": cart[2],
                "price": cart[3],
                "picture": base64.b64encode(cart[4]).decode("utf-8"),
                "quantity": cart[5],
            }
        )

    connection.execute(
        """
    SELECT order_id
    FROM Orders
    
    WHERE Orders.customer_id = ?
    """,
        (int(customer_information[0]),),
    )
    order_id = connection.fetchone()

    for o in order_id:
        order_id2 = o

    for product_list2 in range(len(product_list)):

        connection.execute(
            "INSERT INTO Order_Details (order_id,product_id,quantity,unit_price) VALUES (?,?,?,?)",
            (
                order_id2,
                product_list[product_list2]["product_id"],
                product_list[product_list2]["quantity"],
                product_list[product_list2]["price"],
            ),
        )

    connection.execute(
        """
    DELETE FROM cart
    WHERE customer_id = :customer_id
    """,
        {"customer_id": int(customer_information[0])},
    )
    conn.commit()

    return render_template("pages/end-payment.html")


if __name__ == "__main__":
    app.run(debug=True)
