
import unicodedata
from decimal import Decimal, ROUND_HALF_UP

from schemas import (
    MonHocKetQua,
    SinhVienDauVao,
    SinhVienKetQua,
    ThongKeNhom,
)

#tính điểm tổng kết một môn
def tinh_diem_mon(diem_40: float, diem_60: float) -> float:
    diem = (
        Decimal(str(diem_40)) * Decimal("0.4")
        + Decimal(str(diem_60)) * Decimal("0.6")
    )

    diem_lam_tron = diem.quantize(
        Decimal("0.1"),
        rounding=ROUND_HALF_UP,
    )

    return float(diem_lam_tron)

#tính trung bình các điểm môn
def tinh_gpa(danh_sach_diem: list[float]) -> float:
    if not danh_sach_diem:
        raise ValueError("Danh sách điểm không được rỗng.")

    tong_diem = Decimal("0")

    for diem in danh_sach_diem:
        tong_diem += Decimal(str(diem))

    diem_trung_binh = tong_diem / Decimal(len(danh_sach_diem))

    gpa = diem_trung_binh.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return float(gpa)

#xử lý toàn bộ môn học của một sinh viên
def tinh_ket_qua_sinh_vien(
    sinh_vien: SinhVienDauVao,
) -> SinhVienKetQua:
    danh_sach_ket_qua = []
    danh_sach_diem = []

    for mon in sinh_vien.danh_sach_mon:
        diem_tong_ket = tinh_diem_mon(
            mon.diem_40,
            mon.diem_60,
        )

        ket_qua_mon = MonHocKetQua(
            ten_mon=mon.ten_mon,
            diem_40=mon.diem_40,
            diem_60=mon.diem_60,
            diem_tong_ket=diem_tong_ket,
        )

        danh_sach_ket_qua.append(ket_qua_mon)
        danh_sach_diem.append(diem_tong_ket)

    return SinhVienKetQua(
        mssv=sinh_vien.mssv,
        ho_ten=sinh_vien.ho_ten,
        danh_sach_mon=danh_sach_ket_qua,
        gpa=tinh_gpa(danh_sach_diem),
    )

def chuan_hoa_tim_kiem(van_ban: str) -> str:
    van_ban = van_ban.casefold().replace("đ", "d")

    van_ban = unicodedata.normalize("NFD", van_ban)

    van_ban = "".join(
        ky_tu
        for ky_tu in van_ban
        if not unicodedata.combining(ky_tu)
    )

    return " ".join(van_ban.split())


def tim_kiem_sinh_vien(
    danh_sach_sinh_vien: list[SinhVienKetQua],
    tu_khoa: str,
) -> list[SinhVienKetQua]:
    tu_khoa = chuan_hoa_tim_kiem(tu_khoa)

    if not tu_khoa:
        return danh_sach_sinh_vien

    ket_qua = []

    for sinh_vien in danh_sach_sinh_vien:
        mssv = chuan_hoa_tim_kiem(sinh_vien.mssv)
        ho_ten = chuan_hoa_tim_kiem(sinh_vien.ho_ten)

        if tu_khoa in mssv or tu_khoa in ho_ten:
            ket_qua.append(sinh_vien)

    return ket_qua

def sap_xep_sinh_vien_theo_gpa(
    danh_sach_sinh_vien: list[SinhVienKetQua],
    giam_dan: bool = True,
) -> list[SinhVienKetQua]:
    return sorted(
        danh_sach_sinh_vien,
        key=lambda sinh_vien: sinh_vien.gpa,
        reverse=giam_dan,
    )

def thong_ke_nhom_sinh_vien(
    danh_sach_sinh_vien: list[SinhVienKetQua],
) -> ThongKeNhom:
    if not danh_sach_sinh_vien:
        return ThongKeNhom(
            so_luong_sinh_vien=0,
        )

    danh_sach_gpa = [
        sinh_vien.gpa
        for sinh_vien in danh_sach_sinh_vien
    ]

    gpa_cao_nhat = max(danh_sach_gpa)
    gpa_thap_nhat = min(danh_sach_gpa)
    gpa_trung_binh = tinh_gpa(danh_sach_gpa)

    sinh_vien_cao_nhat = [
        sinh_vien
        for sinh_vien in danh_sach_sinh_vien
        if sinh_vien.gpa == gpa_cao_nhat
    ]

    sinh_vien_thap_nhat = [
        sinh_vien
        for sinh_vien in danh_sach_sinh_vien
        if sinh_vien.gpa == gpa_thap_nhat
    ]

    return ThongKeNhom(
        so_luong_sinh_vien=len(danh_sach_sinh_vien),
        gpa_cao_nhat=gpa_cao_nhat,
        gpa_thap_nhat=gpa_thap_nhat,
        gpa_trung_binh=gpa_trung_binh,
        sinh_vien_cao_nhat=sinh_vien_cao_nhat,
        sinh_vien_thap_nhat=sinh_vien_thap_nhat,
    )