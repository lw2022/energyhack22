from flask import Flask, render_template, request, redirect, url_for, send_from_directory, url_for, json
from flask_cors import CORS #comment this on deployment
from flask_restful import reqparse
import sys
import io
import os

app = Flask(__name__, static_url_path='', static_folder='vis')
CORS(app)

# Serve home route
@app.route("/")
def home():
    return Flask.send_from_directory(app.static_folder,'index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)