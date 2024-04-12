from flask import Flask, make_response, request, jsonify, json,render_template,redirect,url_for
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

app = connect_db.app


cors = CORS(app)
app.config["UPLOAD_FOLDER"] = "static/img/"
