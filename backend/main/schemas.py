from pydantic import BaseModel, ConfigDict, Field

class MonHocDauVao(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    ten_mon: str = Field(min_length=1, max_length=100)

    diem_40: float = Field(
        ge=0,
        le=10,
        strict=True,
        allow_inf_nan=False,
    )

    diem_60: float = Field(
        ge=0,
        le=10,
        strict=True,
        allow_inf_nan=False,
    )


class SinhVienDauVao(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    mssv: str = Field(min_length=1, max_length=30)
    ho_ten: str = Field(min_length=1, max_length=100)

    danh_sach_mon: list[MonHocDauVao] = Field(min_length=1)

#lớp kết quả kế thừa các trường của lớp đầu vào
class MonHocKetQua(MonHocDauVao):
    diem_tong_ket: float = Field(ge=0, le=10)

#SinhVienKetQua bổ sung GPA và dùng danh sách môn có điểm tổng kết.
class SinhVienKetQua(SinhVienDauVao):
    danh_sach_mon: list[MonHocKetQua] = Field(min_length=1)
    gpa: float = Field(ge=0, le=10)

class ThongKeNhom(BaseModel):
    so_luong_sinh_vien: int = Field(ge=0)

    gpa_cao_nhat: float | None = None
    gpa_thap_nhat: float | None = None
    gpa_trung_binh: float | None = None

    sinh_vien_cao_nhat: list[SinhVienKetQua] = Field(
        default_factory=list,
    )

    sinh_vien_thap_nhat: list[SinhVienKetQua] = Field(
        default_factory=list,
    )