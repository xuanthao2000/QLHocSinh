from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,Float,DateTime,Enum
from sqlalchemy.orm import relationship # Obj khóa ngoại
from StudentManagement import db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as QuyenEnum

class GiaoVien(db.Model):
    MaGV = Column(Integer, primary_key=True, autoincrement=True)
    TenGV = Column(String(50), nullable=False)


class Lop(db.Model):
    MaLop = Column(Integer, primary_key=True, autoincrement=True)
    TenLop = Column(String(50), nullable=False)
    SiSo = Column(Integer)
    MaKhoi = Column(Integer)
    HocSinhs = relationship('HocSinh', backref='lop', lazy=True) #Đưa vào HS 1 cái obj có thể .id or name or...


class HocSinh(db.Model):
    MaHS = Column(Integer, primary_key=True, autoincrement=True)
    HoTenHS = Column(String(50), nullable=False)
    GioiTinh = Column(Boolean, nullable=False)
    NgaySinh = Column(String(50), nullable=False)
    DiaChi = Column(String(50), nullable=False)
    SDT = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False)
    Lop_Ma = Column(Integer, ForeignKey(Lop.MaLop), nullable=False)




class Khoi(db.Model):
    MaKhoi = Column(Integer, primary_key=True, autoincrement=True)
    TenKhoi = Column(String(50), nullable=False)

class MonHoc(db.Model):
    MaMH = Column(Integer, primary_key=True, autoincrement=True)
    TenMH = Column(String(50), nullable=False)



class Diem(db.Model):
    MaDiem = Column(Integer, primary_key=True, autoincrement=True)
    Diem15p = Column(Integer)
    Diem1Tiet = Column(Integer)
    DiemThi = Column(Integer)
    MaHS = Column(Integer)
    MaMH = Column(Integer)

#Bang tai khoan va quyen
class Quyen(QuyenEnum):
    admin = 1
    nhanVien = 2
    giaoVien = 3

class TaiKhoan(db.Model, UserMixin):
    MaTk = Column(Integer, primary_key=True, autoincrement=True)
    tenDangNhap = Column(String(50), nullable=False, unique=True)
    matKhau = Column(String(50), nullable=False)
    quyen = Column(Enum(Quyen), default=Quyen.giaoVien)
    trangThai = Column(Boolean, default=False)
    ngayThamGia = Column(DateTime)

    def __str__(self):
        return self.tenDangNhap


if __name__ == '__main__':
    db.create_all()