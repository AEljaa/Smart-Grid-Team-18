from flask import Flask, render_template, redirect, request, url_for, request, session, send_file
from functools import wraps
import os
import sqlite3
app = Flask(__name__, template_folder="templates")

@app.route('/')
@app.route('/home')
def home():
   return render_template('home.html')

@app.route('/current_prices', methods=['GET','POST'])
def current_prices():
    return render_template('current_prices.html',  webshowcurrentbuyprice = "666", webshowcurrentsellprice = "6", webshowcurrentdemand="3", webshowcurrentlightinsesity ="4")

@app.route("/Histroy")
def History():
   return render_template("history.html",rows=[] )

if __name__ == '__main__':
   app.run(debug=True)