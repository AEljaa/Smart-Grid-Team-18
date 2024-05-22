from flask import Flask, render_template, redirect, request, url_for, request, session, send_file
from functools import wraps
import os
import sqlite3
app = Flask(__name__, template_folder="templates")

@app.route('/')
@app.route('/home')
def home():
   return render_template('home.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')



if __name__ == '__main__':
   app.run(debug=True)