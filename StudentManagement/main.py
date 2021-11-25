from flask import render_template,request,redirect
from StudentManagement import app, login
from flask_login import login_user,logout_user
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

    user = DAO.check_login(username=username, password=password)

    if user:
        login_user(user=user)

    return redirect('/admin')

@app.route('/admin/register', methods=['get', 'post'])
def register():
    err_msg =""
    if request.method.__eq__('POST'):
        try:
            name = request.form['name']
            gender = request.form['gender']
            birthday = request.form['birthday']
            phone = request.form['phone']
            email = request.form['email']

            if DAO.register_teacher(name=name, gender=gender, birthday=birthday, phone=phone, email=email):
                err_msg = "Tạo tài khoản thành công"
            else:
                err_msg = "Tạo tài khoản không thành công"
        except Exception as ex:
            error_msg = str(ex)

    return render_template('/admin/Register.html', err_msg=err_msg)

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    logout_user()

    return redirect('/admin')

if __name__ == "__main__":
    app.run(debug=True)

