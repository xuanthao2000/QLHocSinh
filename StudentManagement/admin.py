import datetime
from StudentManagement import admin, db, DAO
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect, request
from StudentManagement.models import Account, Role, ClassRoom, Student, Semester, Score, Subject

class AdminAuthModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(Role.ADMIN)

class AccountView(AdminAuthModelView):
    column_display_pk = False
    can_view_details = False
    column_searchable_list = ['username']
    column_sortable_list = []
    column_labels = {
        'username': 'Tên tài khoản',
        'password': 'Mật khẩu',
        'user_role': 'Quyền',
        'isActive': 'Trạng thái',
        'jone_date': 'Ngày tạo'
    }

class ClassRoomView(AdminAuthModelView):
    column_display_pk = True
    can_view_details = True
    column_labels = {
        'id': 'Mã lớp',
        'name': 'Tên lớp',
        'number_of_students': 'Sỉ số'
    }
    column_sortable_list = ['id', 'name', 'number_of_students']

class SubjectView(AdminAuthModelView):
    column_display_pk = True
    column_labels = {
        'id': 'Mã môn học',
        'name': 'Tên môn học',
    }

class StudentView(AdminAuthModelView):
    column_display_pk = True
    can_view_details = True
    column_labels = {
        'id': 'Mã học sinh',
        'name': 'Tên học sinh',
        'birthday': 'Ngày sinh',
        'address': 'Địa chỉ',
        'gender': 'Giới tính',
        'class_room': 'Lớp'
    }


class SemesterView(AdminAuthModelView):
    column_display_pk = True
    column_labels = {
        'name': 'Tên học kì',
        'school_year': 'Năm học',
        'from_date': 'Ngày bắt đầu',
        'to_date': 'Ngày kết thúc'
    }

class ScoreView(AdminAuthModelView):
    column_display_pk = False
    column_labels = {
        'score_15_1': 'Điểm 15 phút lần 1',
        'score_15_2': 'Điểm 15 phút lần 2',
        'score_15_3': 'Điểm 15 phút lần 3',
        'score_15_4': 'Điểm 15 phút lần 4',
        'score_15_5': 'Điểm 15 phút lần 5',
        'score_60_1': 'Điểm 1 tiết lần 1',
        'score_60_2': 'Điểm 1 tiết lần 2',
        'score_60_3': 'Điểm 1 tiết lần 3',
        'score_final_exam': 'Điểm cuối kì',
        'score_avg': 'Điểm trung bình',
        'semester': 'Học kì',
        'student': 'Học sinh',
        'subject': 'Môn học'
    }
    column_filters = ['subject']


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        semester = request.args.get('semester')
        subject = request.args.get('subject')
        year = request.args.get('year')

        return self.render('admin/stats.html',
                           stats=DAO.class_room_stats(semester, subject, year),
                           semesters=DAO.get_all_semester(),
                           subjects=DAO.get_all_subject())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(Role.ADMIN)


admin.add_view(AccountView(Account, db.session, name='Tài khoản'))
admin.add_view(ClassRoomView(ClassRoom, db.session, name='Lớp'))
admin.add_view(StudentView(Student, db.session, name='Học sinh'))
admin.add_view(SemesterView(Semester, db.session, name='Học kì'))
admin.add_view(SubjectView(Subject, db.session, name='Môn học'))


admin.add_view(ScoreView(Score, db.session, name='Điểm'))



admin.add_view(StatsView(name='Thống kê'))


admin.add_view(LogoutView(name='Đăng xuất'))





