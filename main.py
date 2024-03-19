from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3
import connect_db as connect_db
import user_acount as user_acount
import admin as admin
import base64

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


@app.route("/home/category/<int:category_id>")
def product(category_id):
    if len(customer_information) == 0:
        return redirect(url_for("login"))
    else:
        connection.execute(
            """
        SELECT Products.product_id, Products.name, Products.description, Products.price, Products.picture
        FROM Products
        INNER JOIN Categories
        ON Products.categories_id = Categories.category_id
        WHERE category_id = ?
        """,
            (category_id,),  # Pass category_id as a tuple
        )
    products = connection.fetchall()
    connection.execute(
        "SELECT name FROM Categories WHERE category_id = ?", (str(category_id),)
    )
    category_name = connection.fetchone()

    product_list = []

    for product in products:
        picture_base64 = base64.b64encode(product[4]).decode("utf-8")
        product_list.append(
            {
                "product_id": product[0],
                "name": product[1],
                "description": product[2],
                "price": product[3],
                "picture": picture_base64,
            }
        )
    return render_template(
        "pages/product.html", product_list=product_list, category_name=category_name[0]
    )


def cart(product_id):
    connection.execute(
        "INSERT INTO cart (customer_id,product_id,quantity) VALUES (?,?,?)",
        (customer_information[0], product_id, 1),
    )
    conn.commit()


@app.route("/home/product-details/<int:id>", methods=["POST", "GET"])
def product_details(id):
    if len(customer_information) == 0:
        return redirect(url_for("login"))
    else:
        connection.execute(
            """SELECT product_id, name, description, price, picture FROM Products WHERE product_id = ? """,
            (id,),
        )
        product = connection.fetchone()

        product_data = {
            "product_id": product[0],
            "name": product[1],
            "description": product[2],
            "price": product[3],
            "picture": base64.b64encode(product[4]).decode("utf-8"),
        }
        if request.method == "POST":
            cart(product_data["product_id"])
        return render_template("pages/product-details.html", product_data=product_data)


@app.route("/cart/", methods=["POST", "GET"])
def user_cart():
    if len(customer_information) == 0:
        return redirect(url_for("login"))
    else:
        connection.execute(
            """SELECT Products.product_id,Products.name,Products.description,Products.price,Products.picture
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
                }
            )
        return render_template(
            "pages/cart.html",
            product_list=product_list,
        )


if __name__ == "__main__":
    app.run(debug=True)
