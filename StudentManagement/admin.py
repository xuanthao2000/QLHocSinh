from StudentManagement import admin, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user
from flask import redirect

# admin.add_view(ModelView(MonHoc, db.session, name='Môn học'))


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

admin.add_view(LogoutView(name='Đăng xuất'))





