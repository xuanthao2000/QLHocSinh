from StudentManagement import admin, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect
from StudentManagement.models import Account, Role, ClassRoom, Student

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


class RegisterView(BaseView):
    @expose('/')
    def index(self):
        return self.render('/admin/Register.html')

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AccountView(Account, db.session, name='Tài khoản'))
admin.add_view(ClassRoomView(ClassRoom, db.session, name='Lớp'))
admin.add_view(AdminAuthModelView(Student, db.session, name='Học sinh'))



#admin.add_view(RegisterView(name='Đăng ký', endpoint='register'))

admin.add_view(LogoutView(name='Đăng xuất'))





