from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship, backref
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
    teacher = relationship('Teacher', backref=backref('Account', uselist=False), lazy=True)
    employee = relationship('Employee', backref=backref('Account', uselist=False), lazy=True)

    def __str__(self):
        return self.username


class Teacher(BaseModel):
    name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    birthday = Column(DateTime, default=datetime.now())
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    account_id = Column(Integer, ForeignKey(Account.id))

    def __str__(self):
        return self.name


class Employee(BaseModel):
    name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    birthday = Column(DateTime, default=datetime.now())
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    account_id = Column(Integer, ForeignKey(Account.id))

    def __str__(self):
        return self.name


class Semester(BaseModel):
    __tablename__ = 'semester'
    name = Column(String(25), default='HK1', nullable=False)
    school_year = Column(String(25), nullable=False)
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    scores = relationship('Score', backref='semester', lazy=False)

    def __str__(self):
        return self.name


class ClassRoom(BaseModel):
    __tablename__ = 'class_room'
    name = Column(String(25), nullable=False)
    number_of_students = Column(Integer, default=0)
    students = relationship('Student', backref='class_room', lazy=True)
    teachers = relationship('Teacher', secondary='class_room_teacher', lazy='subquery',
                            backref=backref('class_room', lazy=True))

    def __str__(self):
        return self.name


class_room_teacher = db.Table(
    'class_room_teacher',
    Column('class_room_id', Integer, ForeignKey(ClassRoom.id), primary_key=True),
    Column('teacher_id', Integer, ForeignKey(Teacher.id), primary_key=True)
)


class Student(BaseModel):
    __tablename__ = 'student'
    name = Column(String(25), nullable=False)
    email = Column(String(25), nullable=False, unique=True)
    birthday = Column(DateTime)
    address = Column(String(100))
    gender = Column(String(10))
    phone = Column(String(10))
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
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False, primary_key=True)
    score_15_1 = Column(Float, default=0)
    score_15_2 = Column(Float, default=0)
    score_15_3 = Column(Float, default=0)
    score_15_4 = Column(Float, default=0)
    score_15_5 = Column(Float, default=0)
    score_60_1 = Column(Float, default=0)
    score_60_2 = Column(Float, default=0)
    score_60_3 = Column(Float, default=0)
    score_final_exam = Column(Float, default=0)
    score_avg = Column(Float, default=0)


if __name__ == '__main__':
    db.create_all()

    admin = Account(username='admin', password='202cb962ac59075b964b07152d234b70', user_role='1')
    db.session.add(admin)
    db.session.commit()

    semester1 = Semester(name='HK1-2021', school_year='2021', from_date='2021-01-01 00:00:00',
                         to_date='2021-06-01 00:00:00')
    semester2 = Semester(name='HK2-2021', school_year='2021', from_date='2021-06-02 00:00:00',
                         to_date='2021-12-01 00:00:00')
    semester3 = Semester(name='HK1-2022', school_year='2022', from_date='2022-01-01 00:00:00',
                         to_date='2022-06-01 00:00:00')
    semester4 = Semester(name='HK2-2022', school_year='2022', from_date='2022-06-02 00:00:00',
                         to_date='2022-12-01 00:00:00')

    db.session.add(semester1)
    db.session.add(semester2)
    db.session.add(semester3)
    db.session.add(semester4)

    db.session.commit()

    c1 = ClassRoom(name='10a1', number_of_students=4)
    c2 = ClassRoom(name='10a2', number_of_students=4)
    c3 = ClassRoom(name='11a1', number_of_students=2)
    c4 = ClassRoom(name='11a2', number_of_students=2)
    c5 = ClassRoom(name='12a1', number_of_students=1)
    c6 = ClassRoom(name='12a2', number_of_students=1)

    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.add(c5)
    db.session.add(c6)

    db.session.commit()

    student1 = Student(name='Trần Nhật Long', email='nhatlong1826@gmail.com',
                       birthday='2004-02-20 00:00:00', gender='nam', phone='123456', address='test', classRoom_id=1)
    student2 = Student(name='test1', email='test1@gmail.com',
                       birthday='2004-02-20 00:00:00', gender='nam', phone='123456', address='test', classRoom_id=1)
    student3 = Student(name='test2', email='test2@gmail.com',
                       birthday='2004-02-20 00:00:00', gender='nam', phone='123456', address='test', classRoom_id=1)
    student4 = Student(name='test3', email='test3@gmail.com',
                       birthday='2004-02-20 00:00:00', gender='nam', phone='123456', address='test', classRoom_id=1)
    student5 = Student(name='Nguyễn Xuân Thao', email='thaothao@gmail.com',
                       birthday='2004-02-20 00:00:00', gender='nam', phone='123456', address='test', classRoom_id=2)
    student6 = Student(name='test4', email='test4@gmail.com',
                       birthday='2004-02-20 00:00:00', gender='nam', phone='123456', address='test', classRoom_id=2)
    student7 = Student(name='test5', email='test5@gmail.com',
                       birthday='2018-02-20 00:00:00', gender='nam', phone='123456', address='test', classRoom_id=2)
    student8 = Student(name='test6', email='test6@gmail.com',
                       birthday='2005-02-20 00:00:00', gender='nam', phone='123456', address='test', classRoom_id=2)
    student9 = Student(name='test9', email='test9@gmail.com',
                       birthday='2005-02-20 00:00:00', gender='nam', phone='123456', address='test', classRoom_id=3)
    student10 = Student(name='test10', email='test10@gmail.com',
                        birthday='2005-02-20 00:00:00', gender='nữ', phone='123456', address='test', classRoom_id=3)
    student11 = Student(name='test11', email='test11@gmail.com',
                        birthday='2005-02-20 00:00:00', gender='nữ', phone='123456', address='test', classRoom_id=4)
    student12 = Student(name='test12', email='test12@gmail.com',
                        birthday='2005-02-20 00:00:00', gender='nữ', phone='123456', address='test', classRoom_id=4)
    student13 = Student(name='test13', email='test13@gmail.com',
                        birthday='2004-02-20 00:00:00', gender='nữ', phone='123456', address='test', classRoom_id=5)
    student14 = Student(name='test14', email='test14@gmail.com',
                        birthday='2004-02-20 00:00:00', gender='nam', phone='123456', address='test', classRoom_id=6)
    student15 = Student(name='test15', email='test15@gmail.com',
                       birthday='2004-02-20 00:00:00', gender='nữ', phone='123456', address='test')
    student16 = Student(name='test16', email='test16@gmail.com',
                       birthday='2004-02-20 00:00:00', gender='nam', phone='123456', address='test')
    student17 = Student(name='test17', email='test17@gmail.com',
                        birthday='2004-02-20 00:00:00', gender='nữ', phone='123456', address='test')
    student18 = Student(name='test18', email='test18@gmail.com',
                        birthday='2005-02-20 00:00:00', gender='nữ', phone='123456', address='test')
    student19 = Student(name='test19', email='test19@gmail.com',
                        birthday='2005-02-20 00:00:00', gender='nữ', phone='123456', address='test')
    student20 = Student(name='test20', email='test20@gmail.com',
                        birthday='2005-02-20 00:00:00', gender='nữ', phone='123456', address='test')
    student21 = Student(name='test21', email='test21@gmail.com',
                        birthday='2005-02-20 00:00:00', gender='nam', phone='123456', address='test')

    db.session.add(student1)
    db.session.add(student2)
    db.session.add(student3)
    db.session.add(student4)
    db.session.add(student5)
    db.session.add(student6)
    db.session.add(student7)
    db.session.add(student8)
    db.session.add(student9)
    db.session.add(student10)
    db.session.add(student11)
    db.session.add(student12)
    db.session.add(student13)
    db.session.add(student14)
    db.session.add(student15)
    db.session.add(student16)
    db.session.add(student17)
    db.session.add(student18)
    db.session.add(student19)
    db.session.add(student20)
    db.session.add(student21)
    db.session.commit()

    subject1 = Subject(name='Toán')
    subject2 = Subject(name='Lý')
    subject3 = Subject(name='Hóa')
    subject4 = Subject(name='Văn')
    subject5 = Subject(name='Sinh')
    subject6 = Subject(name='Tiếng anh')

    db.session.add(subject1)
    db.session.add(subject2)
    db.session.add(subject3)
    db.session.add(subject4)
    db.session.add(subject5)
    db.session.add(subject6)

    db.session.commit()

    score1 = Score(student_id=1, subject_id=1, semester_id=1,
                   score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                   score_60_1=7, score_60_2=7, score_60_3=7,
                   score_final_exam=7,
                   score_avg=7.7)
    score2 = Score(student_id=1, subject_id=2, semester_id=1,
                   score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                   score_60_1=7, score_60_2=7, score_60_3=7,
                   score_final_exam=7,
                   score_avg=7.7)
    score3 = Score(student_id=1, subject_id=3, semester_id=1,
                   score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                   score_60_1=7, score_60_2=7, score_60_3=7,
                   score_final_exam=7,
                   score_avg=7.7)

    score4 = Score(student_id=2, subject_id=1, semester_id=1,
                   score_15_1=4, score_15_2=2, score_15_3=3, score_15_4=1, score_15_5=5,
                   score_60_1=3, score_60_2=5, score_60_3=2,
                   score_final_exam=5,
                   score_avg=4.2)
    score5 = Score(student_id=2, subject_id=2, semester_id=1,
                   score_15_1=4, score_15_2=2, score_15_3=3, score_15_4=1, score_15_5=5,
                   score_60_1=3, score_60_2=5, score_60_3=2,
                   score_final_exam=5,
                   score_avg=4.2)
    score6 = Score(student_id=2, subject_id=3, semester_id=1,
                   score_15_1=7, score_15_2=8, score_15_3=7, score_15_4=8, score_15_5=7,
                   score_60_1=8, score_60_2=7, score_60_3=8,
                   score_final_exam=8,
                   score_avg=7.8)

    score7 = Score(student_id=3, subject_id=1, semester_id=1,
                   score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                   score_60_1=7, score_60_2=7, score_60_3=7,
                   score_final_exam=7,
                   score_avg=7.7)
    score8 = Score(student_id=3, subject_id=2, semester_id=1,
                   score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                   score_60_1=7, score_60_2=7, score_60_3=7,
                   score_final_exam=7,
                   score_avg=7.7)
    score9 = Score(student_id=3, subject_id=3, semester_id=1,
                   score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                   score_60_1=7, score_60_2=7, score_60_3=7,
                   score_final_exam=7,
                   score_avg=7.7)

    score10 = Score(student_id=4, subject_id=1, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score11 = Score(student_id=4, subject_id=2, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score12 = Score(student_id=4, subject_id=3, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    # Lop a2
    score13 = Score(student_id=5, subject_id=1, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score14 = Score(student_id=5, subject_id=2, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score15 = Score(student_id=5, subject_id=3, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score16 = Score(student_id=6, subject_id=1, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score17 = Score(student_id=6, subject_id=2, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score18 = Score(student_id=6, subject_id=3, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score19 = Score(student_id=7, subject_id=1, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score20 = Score(student_id=7, subject_id=2, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score21 = Score(student_id=7, subject_id=3, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score22 = Score(student_id=8, subject_id=1, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score23 = Score(student_id=8, subject_id=2, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score24 = Score(student_id=8, subject_id=3, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    # hk2
    score25 = Score(student_id=9, subject_id=1, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score26 = Score(student_id=9, subject_id=2, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score27 = Score(student_id=9, subject_id=3, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score28 = Score(student_id=9, subject_id=1, semester_id=2,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score29 = Score(student_id=9, subject_id=2, semester_id=2,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score30 = Score(student_id=9, subject_id=3, semester_id=2,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score31 = Score(student_id=10, subject_id=1, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score32 = Score(student_id=10, subject_id=2, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score33 = Score(student_id=10, subject_id=3, semester_id=1,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score34 = Score(student_id=10, subject_id=1, semester_id=2,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score35 = Score(student_id=10, subject_id=2, semester_id=2,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    score36 = Score(student_id=10, subject_id=3, semester_id=2,
                    score_15_1=7, score_15_2=7, score_15_3=7, score_15_4=8, score_15_5=7,
                    score_60_1=7, score_60_2=7, score_60_3=7,
                    score_final_exam=7,
                    score_avg=7.7)
    db.session.add(score1)
    db.session.add(score2)
    db.session.add(score3)
    db.session.add(score4)
    db.session.add(score5)
    db.session.add(score6)
    db.session.add(score7)
    db.session.add(score8)
    db.session.add(score9)
    db.session.add(score10)
    db.session.add(score11)
    db.session.add(score12)
    db.session.add(score13)
    db.session.add(score14)
    db.session.add(score15)
    db.session.add(score16)
    db.session.add(score17)
    db.session.add(score18)
    db.session.add(score19)
    db.session.add(score20)
    db.session.add(score21)
    db.session.add(score22)
    db.session.add(score23)
    db.session.add(score24)
    db.session.add(score25)
    db.session.add(score26)
    db.session.add(score27)
    db.session.add(score28)
    db.session.add(score29)
    db.session.add(score30)
    db.session.add(score31)
    db.session.add(score32)
    db.session.add(score33)
    db.session.add(score34)
    db.session.add(score35)
    db.session.add(score36)
    db.session.commit()
