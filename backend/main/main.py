from typing import Literal
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI, HTTPException, Response
from starlette.types import Scope


from schemas import (
    SinhVienDauVao,
    SinhVienKetQua,
    ThongKeNhom,
)

from services import (
    tinh_ket_qua_sinh_vien,
    tim_kiem_sinh_vien,
    sap_xep_sinh_vien_theo_gpa,
    thong_ke_nhom_sinh_vien,
)

from storage import cap_nhat_sinh_vien, doc_du_lieu, them_sinh_vien

app = FastAPI(
    title = "API Quản lý kết quả học tập",
    description = "Xử lý dữ liệu có cấu trúc với JSON",
    version = "1.0.0",
)

@app.get("/")
def trang_chu():
    return { "thong_bao" : "API Quản lý kết quả học tập" }

@app.post("/students/validate", response_model=SinhVienDauVao)
def kiem_tra_sinh_vien(sinh_vien: SinhVienDauVao):
    return sinh_vien

@app.post(
    "/students/calculate",
    response_model=SinhVienKetQua,
)
def tinh_ket_qua(sinh_vien: SinhVienDauVao):
    return tinh_ket_qua_sinh_vien(sinh_vien)

@app.get(
    "/students",
    response_model=list[SinhVienKetQua],
)
def lay_danh_sach_sinh_vien(
    tu_khoa: str | None = None,
    thu_tu: Literal["tang", "giam"] = "giam",
):
    try:
        danh_sach_sinh_vien = doc_du_lieu()

        if tu_khoa is not None:
            danh_sach_sinh_vien = tim_kiem_sinh_vien(
                danh_sach_sinh_vien,
                tu_khoa,
            )

        danh_sach_sinh_vien = sap_xep_sinh_vien_theo_gpa(
            danh_sach_sinh_vien,
            giam_dan=(thu_tu == "giam"),
        )

        return danh_sach_sinh_vien

    except RuntimeError as loi:
        raise HTTPException(
            status_code=500,
            detail=str(loi),
        ) from loi

@app.post(
    "/students",
    response_model=SinhVienKetQua,
    status_code=201,
)
def tao_sinh_vien(sinh_vien: SinhVienDauVao):
    ket_qua = tinh_ket_qua_sinh_vien(sinh_vien)

    try:
        return them_sinh_vien(ket_qua)

    except ValueError as loi:
        raise HTTPException(
            status_code=409,
            detail=str(loi),
        ) from loi

    except RuntimeError as loi:
        raise HTTPException(
            status_code=500,
            detail=str(loi),
        ) from loi

@app.put("/students", response_model=SinhVienKetQua)
def sua_sinh_vien(mssv_cu: str, sinh_vien: SinhVienDauVao):
    ket_qua = tinh_ket_qua_sinh_vien(sinh_vien)

    try:
        da_luu = cap_nhat_sinh_vien(mssv_cu, ket_qua)
    except ValueError as loi:
        raise HTTPException(status_code=409, detail=str(loi)) from loi
    except RuntimeError as loi:
        raise HTTPException(status_code=500, detail=str(loi)) from loi

    if da_luu is None:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy sinh viên có MSSV {mssv_cu}.",
        )

    return da_luu

@app.get(
    "/students/statistics",
    response_model=ThongKeNhom,
)
def lay_thong_ke():
    try:
        danh_sach_sinh_vien = doc_du_lieu()

        return thong_ke_nhom_sinh_vien(
            danh_sach_sinh_vien,
        )

    except RuntimeError as loi:
        raise HTTPException(
            status_code=500,
            detail=str(loi),
        ) from loi

THU_MUC_GIAO_DIEN = (
    Path(__file__).resolve().parents[2]
    / "frontend"
)

class TepGiaoDien(StaticFiles):
    async def get_response(self, path: str, scope: Scope) -> Response:
        phan_hoi = await super().get_response(path, scope)
        phan_hoi.headers["Cache-Control"] = "no-cache"
        return phan_hoi


app.mount(
    "/web",
    TepGiaoDien(
        directory=THU_MUC_GIAO_DIEN,
        html=True,
    ),
    name="frontend",
)