from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3
import importlib

app = Flask(__name__)
app.config["STATIC_FOLDER"] = "static/img/"
