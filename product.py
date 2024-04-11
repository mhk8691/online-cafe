from datetime import datetime
from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3
import connect_db as connect_db
import user_acount as user_acount
import base64


app = connect_db.app
customer_information = user_acount.customer_information

conn = sqlite3.connect("onlineShop.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
connection = conn.cursor()

category_id = None
product_id = None


def notification_Unread():
    connection.execute(
        "SELECT message,status,created_at FROM Notifications WHERE customer_id = ? AND status = ?",
        (
            customer_information[0],
            "Unread",
        ),
    )

    notification_list = connection.fetchall()
    notification_list2 = []
    for notification in notification_list:
        notification_list2.append(
            {
                "message": notification[0],
                "status": notification[1],
                "created_at": notification[2],
            }
        )

    return notification_list2


# show all product
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
            "SELECT category_name FROM Categories WHERE category_id = ?",
            (str(category_id),),
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
        notification_user2 = notification_Unread()

        if len(notification_user2) == 0:
            display = "d-none"
        else:
            display = "d-block"
    return render_template(
        "pages/product.html",
        product_list=product_list,
        category_name=category_name[0],
        display=display,
    )


# Add to cart
def cart(product_id):
    connection.execute(
        "INSERT INTO cart (customer_id,product_id,quantity) VALUES (?,?,?)",
        (customer_information[0], product_id, 1),
    )
    conn.commit()


# محصولات مشابه
def similar_products(product_id, category_id):
    connection.execute(
        "SELECT * FROM Products INNER JOIN Categories ON Products.categories_id = Categories.category_id WHERE categories_id = ? AND product_id != ? LIMIT 4 ",
        (category_id, product_id),
    )
    product_list = connection.fetchall()
    final_product_list = []
    for product in product_list:
        picture_base64 = base64.b64encode(product[4]).decode("utf-8")
        final_product_list.append(
            {
                "product_id": product[0],
                "name": product[1],
                "description": product[2],
                "price": product[3],
                "picture": picture_base64,
            }
        )
    return final_product_list


# View product_details
@app.route("/home/product-details/<int:id>", methods=["POST", "GET"])
def product_details(id):
    if len(customer_information) == 0:
        return redirect(url_for("login"))
    else:
        connection.execute(
            """SELECT * FROM Products WHERE product_id = ? """,
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
        product_id = product[0]
        category_id = product[5]

        if request.method == "POST":
            cart(product_data["product_id"])

        connection.execute(
            "SELECT * FROM cart WHERE product_id = ? AND customer_id = ?",
            (id, customer_information[0]),
        )
        row = connection.fetchall()
        if len(row) != 0:
            display = "d-none"
            display2 = "d-block"
        else:
            display = "d-block"
            display2 = "d-none"

        # similar_products
        product_list = similar_products(product_id, category_id)
        if len(product_list) == 0:
            display_similar = "d-none"
        else:
            display_similar = "d-block"

        notification_user2 = notification_Unread()

        if len(notification_user2) == 0:
            display_not = "d-none"
        else:
            display_not = "d-block"
        return render_template(
            "pages/product-details.html",
            product_data=product_data,
            display=display,
            display2=display2,
            product_list=product_list,
            display_similar=display_similar,
            display_not=display_not,
        )


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


def show_cart():
    connection.execute(
        """SELECT Products.product_id,Products.name,Products.description,Products.price,Products.picture,quantity
                from Products
                inner join cart
                on cart.product_id = Products.product_id
                where cart.customer_id = ?""",
        (customer_information[0],),
    )
    carts = connection.fetchall()
    return carts


def number_of_cart():
    if request.method == "POST":
        number = request.form["number"]
        product_id = request.form["product_id"]
        if int(number) >= 1:
            connection.execute(
                "UPDATE cart SET quantity = ? WHERE product_id = ? ",
                (number, product_id),
            )
            conn.commit()
        elif int(number) == 0:

            connection.execute(
                "DELETE FROM cart WHERE product_id = ? ",
                (product_id,),
            )
            conn.commit()


# View shopping cart
@app.route("/cart/", methods=["POST", "GET"])
def user_cart():
    if len(customer_information) == 0:
        return redirect(url_for("login"))
    else:
        number_of_cart()

        carts = show_cart()

        if len(carts) == 0:
            display = "d-none"
        else:
            display = "d-block"

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
        list_price2 = Totalprice()
        query = (
            "SELECT * FROM Shipping_Addresses WHERE customer_id = {} LIMIT 1".format(
                customer_information[0]
            )
        )
        connection.execute(query)
        list_address = connection.fetchall()
        shipping_address_defult = []
        if len(list_address) != 0:
            for list in list_address:
                shipping_address_defult.append(
                    {
                        "recipient_name": list[2],
                        "address_line1": list[3],
                        "address_line2": list[4],
                        "city": list[5],
                        "state": list[6],
                        "postal_code": list[7],
                        "country": list[8],
                    }
                )

            print(shipping_address_defult)

        notification_user2 = notification_Unread()

        if len(notification_user2) == 0:
            display_not = "d-none"
        else:
            display_not = "d-block"
        return render_template(
            "pages/cart.html",
            product_list=product_list,
            d="d-none",
            list_price2=list_price2,
            display=display,
            display_not=display_not,
            shipping_address_defult=shipping_address_defult,
        )
