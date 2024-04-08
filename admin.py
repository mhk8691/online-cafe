from flask import Flask, request, jsonify, json
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












# def get_user(user_id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))

#     user = cur.fetchone()

#     final_user = {
#         "id": user[0],
#         "username": user[1],
#         "password": user[2],
#         "email": user[3],
#         "role": user[4],
#     }

#     conn.close()
#     return final_user
