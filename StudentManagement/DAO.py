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

def check_login_emp(username, password, role=Role.EMPLOYEE):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = Account.query.filter(Account.username == username,
                             Account.password == password,
                             Account.user_role == role).first()

    return user

def check_login_admin(username, password, role=Role.ADMIN):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = Account.query.filter(Account.username == username,
                             Account.password == password,
                             Account.user_role == role).first()

    return user

def check_login_teacher(username, password, role=Role.TEACHER):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = Account.query.filter(Account.username == username,
                             Account.password == password,
                             Account.user_role == role).first()

    return user

def register_teacher(name, gender, birthday, phone, email, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(username=username, password=password, user_role=Role.TEACHER)

    teacher = Teacher(name=name, gender=gender, birthday=birthday, email=email, phone=phone)

    try:

        db.session.add(account)
        db.session.commit()

        db.session.add(teacher)
        db.session.commit()

    except:
        return False
    else:
        return True


def register_empoyee(name, gender, birthday, phone, email, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(username=username, password=password, user_role=Role.EMPLOYEE)

    employee = Employee(
        name=name,
        gender=gender,
        birthday=birthday,
        email=email,
        phone=phone)


    try:
        db.session.add(account)
        db.session.commit()

        db.session.add(employee)
        db.session.commit()
    except:
        return False
    else:
        return True

def get_class_room_by_id(id):
    return ClassRoom.query.get(id)

def get_all_semester():
    return Semester.query.all()

def get_all_subject():
    return Subject.query.all()



def class_room_stats(se=None, sub=None, year=None):
    class_room = db.session.query(ClassRoom.name, ClassRoom.number_of_students, func.count(Student.id))\
        .join(Student, ClassRoom.id == Student.classRoom_id)\
        .join(Score, Score.student_id == Student.id)\
        .join(Semester, Semester.id == Score.semester_id)\
        .join(Subject, Subject.id == Score.subject_id)\
        .group_by(ClassRoom.name)


    result = class_room.filter(Score.score_avg >= 5,
                               Semester.id == se,
                               Semester.school_year == year,
                               Subject.id == sub)

    return result.all()