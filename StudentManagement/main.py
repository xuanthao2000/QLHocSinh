from flask import render_template, request, redirect,flash
from StudentManagement import app, login
from flask_login import login_user, logout_user
import DAO
from StudentManagement.admin import *


@app.route('/')
def home():
    return render_template('Home.html')


@login.user_loader
def load_user(user_id):
    return DAO.get_user_by_id(user_id=user_id)


@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = DAO.check_login_admin(username=username, password=password)

    if user:
        login_user(user=user)
    else:
        flash("Sai tên đăng nhập hoặc mật khẩu", "danger")

    return redirect('/admin')


@app.route('/admin/register', methods=['POST'])
def register():
    err_msg = ""
    try:
        account = request.form.get('account')
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        birthday = request.form.get('birthday')
        gender = request.form.get('gender')
        phone = request.form.get('phone')

        print(account, username, email, birthday, gender, phone, username, password)

        if account.__eq__('employee') :
            if DAO.register_empoyee(name=name, gender=gender, birthday=birthday, phone=phone,
                                    email=email, username=username, password=password):
                err_msg = "Tạo tài khoản thành công"
            else:
                err_msg = "Tạo tài khoản không thành công"
        else:
            if account.__eq__('teacher'):
                if DAO.register_teacher(name=name, gender=gender, birthday=birthday, phone=phone,
                                        email=email, username=username, password=password):
                    err_msg = "Tạo tài khoản thành công"
                else:
                    err_msg = "Tạo tài khoản không thành công"
    except Exception as ex:
        error_msg = str(ex)


    #return render_template('/admin/Register.html', err_msg=err_msg)
    return redirect('/admin')


@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    logout_user()

    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True)
