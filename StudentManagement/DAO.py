from StudentManagement.models import Account, Teacher
import hashlib
from StudentManagement import db

def get_user_by_id(user_id):
    return Account.query.get(user_id)

def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return Account.query.filter(Account.username.__eq__(username.strip()),
                                     Account.password.__eq__(password)).first()

def register_teacher(name,gender,birthday,phone,email):

    a = Teacher(
                name=name,
                gender=gender,
                birthday=birthday,
                email=email,
                phone=phone)
    db.session.add(a)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True


