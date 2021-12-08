from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from StudentManagement import db
from datetime import datetime
from flask_login import UserMixin
import enum

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

class Role(enum.Enum):
    ADMIN = 1
    EMPLOYEE = 2
    TEACHER = 3


class Account(BaseModel, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(Role), default=Role.TEACHER)
    isActive = Column(Boolean, default=False)
    jone_date = Column(DateTime, default=datetime.now())
    teacher = relationship('Teacher', backref='Account', lazy=True)
    employee = relationship('Employee', backref='Account', lazy=True)


    def __str__(self):
        return self.username

class Teacher(BaseModel):
    name = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    birthday = Column(DateTime, default=datetime.now())
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    account_id = Column(Integer, ForeignKey(Account.id))


class Employee(BaseModel):
    name = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    birthday = Column(DateTime, default=datetime.now())
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    account_id = Column(Integer, ForeignKey(Account.id))


class ClassRoom(BaseModel):
    __tablename__ = 'class_room'
    name = Column(String(25), nullable=False)
    number_of_students = Column(Integer, default=0)
    students = relationship('Student', backref='class_room', lazy=False)

    def __str__(self):
        return self.name

class Student(BaseModel):
    __tablename__ = 'student'
    name = Column(String(25), nullable=False)
    email = Column(String(25), nullable=False, unique=True)
    birthday = Column(DateTime)
    address = Column(String(100))
    gender = Column(Boolean)
    classRoom_id = Column(Integer, ForeignKey(ClassRoom.id))
    scores = relationship('Score', backref='student', lazy=False)

    def __str__(self):
        return self.name

class Subject(BaseModel):
    __tablename__ = 'subject'
    name = Column(String(25), nullable=False)
    scores = relationship('Score', backref='subject', lazy=False)

    def __str__(self):
        return self.name

class Score(db.Model):
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False, primary_key=True)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False, primary_key=True)
    score_15_1 = Column(Float, default=0)
    score_15_2 = Column(Float, default=0)
    score_15_3 = Column(Float, default=0)
    score_15_4 = Column(Float, default=0)
    score_15_5 = Column(Float, default=0)
    score_60_1 = Column(Float, default=0)
    score_60_2 = Column(Float, default=0)
    score_60_3 = Column(Float, default=0)
    score_final_exam = Column(Float, default=0)



if __name__ == '__main__':
    db.create_all()

    admin = Account(username='admin', password='202cb962ac59075b964b07152d234b70', user_role='1')
    db.session.add(admin)
    db.session.commit()

    c1 = ClassRoom(name='10a1')
    c2 = ClassRoom(name='10a2')
    c3 = ClassRoom(name='11a1')
    c4 = ClassRoom(name='11a2')
    c5 = ClassRoom(name='12a1')
    c6 = ClassRoom(name='12a2')

    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.add(c5)
    db.session.add(c6)

    db.session.commit()