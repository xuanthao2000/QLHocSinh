from pymysql import NULL
from sqlalchemy import func
from StudentManagement.models import Account, Teacher, Employee, Role, ClassRoom, Student, Semester, Subject, Score
import hashlib
from StudentManagement import db


def get_user_by_id(user_id):
    return Account.query.get(user_id)


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return Account.query.filter(Account.username.__eq__(username.strip()),
                                    Account.password.__eq__(password)).first()

def check_login_admin(username, password, role=Role.ADMIN):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = Account.query.filter(Account.username == username,
                             Account.password == password,
                             Account.user_role == role).first()

    return user

# def check_login_emp(username, password, role=Role.EMPLOYEE):
#     password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
#
#     user = Account.query.filter(Account.username == username,
#                                 Account.password == password,
#                                 Account.user_role == role).first()
#
#     return user


# def check_login_teacher(username, password, role=Role.TEACHER):
#     password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
#
#     user = Account.query.filter(Account.username == username,
#                                 Account.password == password,
#                                 Account.user_role == role).first()
#
#     return user


def register_teacher(name, gender, birthday, phone, email, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(username=username, password=password, user_role=Role.TEACHER)

    try:
        db.session.add(account)
        db.session.commit()

        a = Account.query.filter(Account.username == username,
                                 Account.password == password).first()

        teacher = Teacher(name=name, gender=gender, birthday=birthday,
                          email=email, phone=phone, account_id=a.id)

        db.session.add(teacher)
        db.session.commit()

    except:
        return False
    else:
        return True


def register_employee(name, gender, birthday, phone, email, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(username=username, password=password, user_role=Role.EMPLOYEE)

    try:
        db.session.add(account)
        db.session.commit()

        a = Account.query.filter(Account.username == username,
                                 Account.password == password).first()

        employee = Employee(name=name, gender=gender, birthday=birthday,
                            email=email, phone=phone, account_id=a.id)

        db.session.add(employee)
        db.session.commit()
    except:
        return False
    else:
        return True


def check_email_teacher(email):
    return Teacher.query.filter(Teacher.email == email).first()


def check_email_employee(email):
    return Employee.query.filter(Employee.email == email).first()


def check_email_student(email):
    return Student.query.filter(Student.email == email).first()


def get_account_by_username(username):
    return Account.query.filter(Account.username == username).first()


def get_class_room_by_id(id):
    return ClassRoom.query.get(id)


def get_all_class():
    return ClassRoom.query.all()


def get_student_no_class():
    students = db.session.query(Student.id, Student.name).filter(Student.classRoom_id == None)
    return students.all()


def get_all_semester():
    return Semester.query.all()


def get_all_subject():
    return Subject.query.all()


def class_room_stats(se=None, sub=None, year=None):
    class_room = db.session.query(ClassRoom.name, ClassRoom.number_of_students, func.count(Student.id)) \
        .join(Student, ClassRoom.id == Student.classRoom_id) \
        .join(Score, Score.student_id == Student.id) \
        .join(Semester, Semester.id == Score.semester_id) \
        .join(Subject, Subject.id == Score.subject_id) \
        .group_by(ClassRoom.name)

    result = class_room.filter(Score.score_avg >= 5,
                               Semester.id == se,
                               Semester.school_year == year,
                               Subject.id == sub)

    return result.all()


def add_student(name, email, birthday, address, gender, phone):
    student = Student(name=name.strip(), email=email.strip(),
                      birthday=birthday, address=address, gender=gender, phone=phone)
    db.session.add(student)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True

def add_class_to_student(classroom_id, student_id):
    classroom = ClassRoom.query.get(classroom_id)
    classroom.number_of_students = classroom.number_of_students + 1

    student = Student.query.get(student_id)
    student.classRoom_id = classroom_id

    try:
        db.session.commit()
    except:
        return False
    else:
        return True

def remove_class_from_student(classroom_id, student_id):
    student = Student.query.get(student_id)
    student.classRoom_id = None

    classroom = ClassRoom.query.get(classroom_id)
    classroom.number_of_students = classroom.number_of_students - 1

    try:
        db.session.commit()
    except:
        return False
    else:
        return True
