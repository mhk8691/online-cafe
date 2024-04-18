from flask import (
    Flask,
    make_response,
    request,
    jsonify,
    json,
    render_template,
    redirect,
    url_for,
)
import sqlite3
from flask_cors import CORS, cross_origin
import connect_db as connect_db
from datetime import datetime
import os
import base64
import requests


import admin_panel.order
import admin_panel.customer
import admin_panel.product
import admin_panel.category
import admin_panel.shipping
import admin_panel.user
import admin_panel.payment
import admin_panel.order_details
import admin_panel.Feedback
import admin_panel.adminLogs
import admin_panel.notification
import admin_panel.user_login as user_login

app = connect_db.app


cors = CORS(app)
app.config["UPLOAD_FOLDER"] = "static/img/"
user_information = user_login.user_information

def get_db_connection():
    conn = sqlite3.connect("onlineShop.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/KPIs", methods=["GET"])
def get_admin_kpis():
    if len(user_information) != 0:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("select sum(amount) from Payments")
        total_revenue = cur.fetchone()[0]

        cur.execute(
            """
        SELECT 
            strftime('%Y-%m', order_date) AS month,
            COUNT(*) AS sales_count
        FROM 
            Orders
        GROUP BY 
            month
        ORDER BY 
            month
    """
        )
        Orderـnumber = cur.fetchall()
        Orderـnumber_list = [
            {"month": row[0], "Orderـnumber": row[1]} for row in Orderـnumber
        ]

        total = []

        cur.execute(
            """
            SELECT 
                strftime('%Y-%m', order_date) AS month,
                SUM(total_amount) AS total_amount
            FROM 
                Orders
            GROUP BY 
                month
            ORDER BY 
                month
        """
        )

        for row in cur.fetchall():
            month_data = {"month": row[0], "Monthlyـsales": row[1]}
            total.append(month_data)

        kpis = {
            "Orderـnumber": Orderـnumber_list,
            "total-revenue": total_revenue,
            "Monthlyـsales": total,
        }

        return jsonify(kpis), 200
