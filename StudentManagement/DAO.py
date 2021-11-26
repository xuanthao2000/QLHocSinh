from StudentManagement.models import Account, Teacher, Employee, role
import hashlib
from StudentManagement import db



def get_user_by_id(user_id):
    return Account.query.get(user_id)


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return Account.query.filter(Account.username.__eq__(username.strip()),
                                    Account.password.__eq__(password)).first()

def check_login_emp(username, password, role=role.staff):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = Account.query.filter(Account.username == username,
                             Account.password == password,
                             Account.user_role == role).first()

    return user

def check_login_admin(username, password, role=role.admin):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = Account.query.filter(Account.username == username,
                             Account.password == password,
                             Account.user_role == role).first()

    return user

def check_login_teacher(username, password, role=role.teacher):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = Account.query.filter(Account.username == username,
                             Account.password == password,
                             Account.user_role == role).first()

    return user

def register_teacher(name, gender, birthday, phone, email, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(username=username, password=password, user_role=role.teacher)

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
    account = Account(username=username, password=password, user_role=role.staff)

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
