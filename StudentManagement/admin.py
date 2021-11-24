from StudentManagement import admin, db
from StudentManagement.models import MonHoc,HocSinh,Diem,GiaoVien,Khoi,Lop, TaiKhoan
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(MonHoc, db.session, name='Môn học'))
admin.add_view(ModelView(HocSinh, db.session))
admin.add_view(ModelView(Diem, db.session))
admin.add_view(ModelView(GiaoVien, db.session))
admin.add_view(ModelView(Khoi, db.session))
admin.add_view(ModelView(Lop, db.session))
admin.add_view(ModelView(TaiKhoan, db.session))



