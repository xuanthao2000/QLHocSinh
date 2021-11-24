from StudentManagement.models import TaiKhoan
import hashlib

def lay_tai_khoan(MaTk):
    return TaiKhoan.query.get(MaTk)

def kiem_tra_dang_nhap(tenDangNhap, matKhau):
    if tenDangNhap and matKhau:
        matKhau = str(hashlib.md5(matKhau.strip().encode('utf-8')).hexdigest())

        return TaiKhoan.query.filter(TaiKhoan.tenDangNhap.__eq__(tenDangNhap.strip()),
                                     TaiKhoan.matKhau.__eq__(matKhau)).first()
