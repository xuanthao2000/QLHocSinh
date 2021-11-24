from flask import render_template,request,redirect
import utils
from StudentManagement import db
import os
from StudentManagement import app, login
from StudentManagement.admin import *
from flask_login import login_user



@app.route('/')
def home():
    return render_template('Home.html')

# @app.route('/Login')
# def Login():
#     return render_template('Login.html')

@login.user_loader
def load_taiKhoan(MaTk):
    return utils.lay_tai_khoan(MaTk = MaTk)

@app.route('/admin/login', methods=['POST'])
def admin_dangNhap():
    tenDangNhap = request.form.get('tenDangNhap')
    matKhau = request.form.get('matKhau')

    taikhoan = utils.kiem_tra_dang_nhap(tenDangNhap = tenDangNhap, matKhau = matKhau)
    if taikhoan:
        login_user(user = taikhoan)

    return redirect('/admin')

if __name__ == "__main__":
    app.run(debug=True)

