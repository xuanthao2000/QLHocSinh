from flask import render_template, request, redirect, flash, url_for
from StudentManagement import app, login
from flask_login import login_user, logout_user, current_user, login_required
import DAO
from StudentManagement.admin import *
from StudentManagement.models import Account, Role, ClassRoom, Student, Semester, Score, Subject



@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')


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

@app.route('/login', methods=['get', 'post'])
def login():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            username = request.form['username']
            password = request.form['password']

            user = DAO.check_login(username=username, password=password)
            if user:
                login_user(user=user)

                next = request.args.get('next', 'home')
                return redirect(url_for(next))
            else:
                error_msg = "Sai tên đăng nhập hoặc mật khẩu!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', error_msg=error_msg)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['get', 'post'])
def register():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            account = request.form.get('account')
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password')
            confirm = request.form.get('confirm')
            email = request.form.get('email')
            birthday = request.form.get('birthday')
            gender = request.form.get('gender')
            phone = request.form.get('phone')

            if DAO.get_account_by_username(username):
                error_msg = "Tên tài khoản đã tồn tại!!!"
            else:
                if password.__eq__(confirm):
                    if account == 'teacher':
                        if DAO.check_email_teacher(email):
                            error_msg = "Địa chỉ email đã tồn tại!!!"
                        else:
                            if DAO.register_teacher(name, gender, birthday, phone, email, username, password):
                                return redirect(url_for('login'))
                            else:
                                error_msg = "Đã xảy ra lỗi"
                    else:
                        if DAO.check_email_employee(email):
                            error_msg = "Địa chỉ email đã tồn tại!!!"
                        else:
                            if DAO.register_employee(name, gender, birthday, phone, email, username, password):
                                return redirect(url_for('login'))
                            else:
                                error_msg = "Đã xảy ra lỗi"
                else:
                    error_msg = "Mật khẩu không khớp!!!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('register.html', error_msg=error_msg)



@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    logout_user()

    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True)
