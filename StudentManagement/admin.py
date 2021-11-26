from StudentManagement import admin, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user
from flask import redirect
from StudentManagement.models import Account

admin.add_view(ModelView(Account, db.session, name='Tài khoản'))



class RegisterView(BaseView):
    @expose('/')
    def index(self):
        return self.render('/admin/Register.html')

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

admin.add_view(LogoutView(name='Đăng xuất'))
admin.add_view(RegisterView(name='Đăng ký', endpoint='register'))





