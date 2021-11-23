from flask import render_template,request
import utils
from StudentManagement import db
import os
from StudentManagement import app
from StudentManagement.admin import *


@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/Login')
def Login():
    return render_template('Login.html')

if __name__ == "__main__":
    app.run(debug=True)

