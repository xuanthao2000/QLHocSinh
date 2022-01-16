from flask import render_template, request, redirect, flash, url_for, jsonify
from StudentManagement import app, login
from flask_login import login_user, logout_user, current_user, login_required
import DAO
import datetime
from StudentManagement.admin import *
from StudentManagement.models import Account, Role, ClassRoom, Student, Semester, Score, Subject


@app.route('/')
def home():
    return render_template('Home.html', role=Role)


@app.route('/teacher')
def teacher():
    return render_template('teacher.html')


# @app.route('/employee')
# def employee():
#     return render_template('employee.html', class_room=DAO.get_all_class())


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
            if user and user.user_role != Role.ADMIN:
                login_user(user=user)
                if user.user_role == Role.TEACHER:
                    next = request.args.get('next', 'add_score')
                    return redirect(url_for(next))
                if user.user_role == Role.EMPLOYEE:
                    next = request.args.get('next', 'add_student')
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


@app.route('/add_student', methods=['get', 'post'])
def add_student():
    error_msg = ""
    success_msg = ""
    now = datetime.datetime.now()

    if request.method.__eq__('POST'):
        try:
            name = request.form['name']
            email = request.form['email']
            birthday = request.form['birthday']
            address = request.form['address']
            gender = request.form['gender']
            phone = request.form['phone']
            year = int(birthday[0:4])

            if 15 <= (now.today().year - year) <= 20:
                if (DAO.check_email_student(email)):
                    error_msg = "Địa chỉ mail đã tồn tại!!!"
                    return render_template('employee.html', error_msg=error_msg,
                                           class_room=DAO.get_all_class())
                else:
                    if (DAO.add_student(name, email, birthday, address, gender, phone)):
                        success_msg = "Thêm học sinh thành công"
                        return render_template('employee.html', success_msg=success_msg,
                                               class_room=DAO.get_all_class())
                    else:
                        error_msg = "Thêm học sinh thất bại!!!"
                        return render_template('employee.html', error_msg=error_msg,
                                               class_room=DAO.get_all_class())
            else:
                error_msg = 'Độ tuổi không phù hợp'
        except Exception as ex:
            error_msg = str(ex)

    return render_template('employee.html', error_msg=error_msg, success_msg=success_msg,
                           class_room=DAO.get_all_class())


@app.route('/add_class', methods=['get', 'post'])
def add_class():
    error_msg = ""
    success_msg = ""
    if request.method.__eq__('POST'):
        try:
            class_name = request.form['class_name']

            if (DAO.add_class_room(class_name)):
                success_msg = "Thêm thành công"
                return render_template('employee.html', success_msg=success_msg,
                                       class_room=DAO.get_all_class())
            else:
                error_msg = "Thêm thất bại !!!"
                return render_template('employee.html', error_msg=error_msg,
                                       class_room=DAO.get_all_class())
        except Exception as ex:
            error_msg = str(ex)

    return render_template('employee.html', error_msg=error_msg, success_msg=success_msg,
                           class_room=DAO.get_all_class())


@app.route('/classroom/<int:class_id>')
def classDetail(class_id):
    return render_template('classDetail.html', class_room=DAO.get_class_room_by_id(id=class_id),
                           students=DAO.get_student_no_class())


@app.route('/classroom/update', methods=['POST'])
def class_room_update():
    try:
        data = request.json
        classroom_id = data.get('classroom_id')
        student_id = data.get('student_id')

        if (DAO.get_class_room_by_id(classroom_id).number_of_students < 4):
            if (DAO.add_class_to_student(classroom_id, student_id)):
                return jsonify({'code': 200})
        else:
            return jsonify({'code': 400, 'err': 'Lớp đã đủ sỉ số'})
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@app.route('/classroom/removeStudent', methods=['POST'])
def remove_student_from_class():
    try:
        data = request.json
        classroom_id = data.get('classroom_id')
        student_id = data.get('student_id')

        if (DAO.remove_class_from_student(classroom_id, student_id)):
            return jsonify({'code': 200})
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@app.route('/remove_class', methods=['post'])
def remove_class():
    error_msg = ""
    success_msg = ""
    if request.method.__eq__('POST'):
        try:
            class_id = request.form['class_id']
            if (DAO.remove_class_room(class_id)):
                success_msg = "Xóa thành công"
                return render_template('employee.html', success_msg=success_msg,
                                       class_room=DAO.get_all_class())
            else:
                error_msg = "Xóa thất bại !!!"
                return render_template('employee.html', error_msg=error_msg,
                                       class_room=DAO.get_all_class())
        except Exception as ex:
            error_msg = str(ex)

    return render_template('employee.html', error_msg=error_msg, success_msg=success_msg,
                           class_room=DAO.get_all_class())


@app.route('/add_score', methods=['get', 'post'])
def add_score():
    error_msg = ""
    success_msg = ""
    if request.method.__eq__('GET'):
        try:
            class_id = request.form['class_id']

            print(class_id)

            # if (DAO.add_class_room(class_name)):
            #     success_msg = "Thêm thành công"
            #     return render_template('teacher.html', success_msg=success_msg,
            #                            class_room=DAO.get_all_class())
            # else:
            #     error_msg = "Thêm thất bại !!!"
            #     return render_template('teacher.html', error_msg=error_msg,
            #                            class_room=DAO.get_all_class())
        except Exception as ex:
            error_msg = str(ex)

    return render_template('teacher.html', error_msg=error_msg, success_msg=success_msg,
                           semester=DAO.get_all_semester(), class_room=DAO.get_all_class(),
                           subjects=DAO.get_all_subject())


@app.route('/show_score', methods=['post'])
def show_score():
    array = []
    if request.method.__eq__('POST'):
        try:
            class_id = request.form['class_id']
            subject_id = request.form['subject_id']
            semester_id = request.form['semester_id']
            class_room = DAO.get_class_room_by_id(class_id)

            for c in class_room.students:
                item = DAO.get_score(subject_id, c.id, semester_id)
                array.append(item)

        except Exception as ex:
            error_msg = str(ex)

    return render_template('teacher.html', scores=array, semester=DAO.get_all_semester(),
                           class_room=DAO.get_all_class(), subjects=DAO.get_all_subject(),
                           )


if __name__ == "__main__":
    app.run(port=3000, debug=True)
