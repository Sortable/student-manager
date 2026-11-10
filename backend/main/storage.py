import json
from pathlib import Path
from threading import RLock

from schemas import SinhVienKetQua


TEP_DU_LIEU = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "sinh_vien.json"
)

KHOA_DU_LIEU = RLock()


def doc_du_lieu() -> list[SinhVienKetQua]:
    with KHOA_DU_LIEU:
        try:
            with TEP_DU_LIEU.open(
                "r",
                encoding="utf-8",
            ) as tep:
                du_lieu = json.load(tep)

            if not isinstance(du_lieu, list):
                raise ValueError("Dữ liệu phải là một danh sách.")

            return [
                SinhVienKetQua.model_validate(sinh_vien)
                for sinh_vien in du_lieu
            ]

        except FileNotFoundError:
            return []

        except (OSError, ValueError) as loi:
            raise RuntimeError(
                "Không thể đọc dữ liệu sinh viên. "
                "Hãy kiểm tra nội dung và quyền truy cập file JSON."
            ) from loi


def ghi_du_lieu(
    danh_sach_sinh_vien: list[SinhVienKetQua],
) -> None:
    with KHOA_DU_LIEU:
        tep_tam = TEP_DU_LIEU.with_suffix(".tmp")

        try:
            TEP_DU_LIEU.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            du_lieu = [
                sinh_vien.model_dump(mode="json")
                for sinh_vien in danh_sach_sinh_vien
            ]

            with tep_tam.open(
                "w",
                encoding="utf-8",
            ) as tep:
                json.dump(
                    du_lieu,
                    tep,
                    ensure_ascii=False,
                    indent=2,
                    allow_nan=False,
                )

            tep_tam.replace(TEP_DU_LIEU)

        except (OSError, ValueError) as loi:
            raise RuntimeError(
                "Không thể lưu dữ liệu sinh viên."
            ) from loi


def them_sinh_vien(
    sinh_vien: SinhVienKetQua,
) -> SinhVienKetQua:
    with KHOA_DU_LIEU:
        danh_sach_sinh_vien = doc_du_lieu()

        for sinh_vien_da_luu in danh_sach_sinh_vien:
            if (
                sinh_vien_da_luu.mssv.casefold()
                == sinh_vien.mssv.casefold()
            ):
                raise ValueError(
                    f"MSSV {sinh_vien.mssv} đã tồn tại."
                )

        danh_sach_sinh_vien.append(sinh_vien)
        ghi_du_lieu(danh_sach_sinh_vien)

        return sinh_vien

def cap_nhat_sinh_vien(
    mssv_cu: str,
    sinh_vien: SinhVienKetQua,
) -> SinhVienKetQua | None:
    ma_cu = mssv_cu.strip().casefold()
    ma_moi = sinh_vien.mssv.casefold()

    with KHOA_DU_LIEU:
        danh_sach = doc_du_lieu()

        for vi_tri, ban_cu in enumerate(danh_sach):
            if ban_cu.mssv.casefold() != ma_cu:
                continue

            if any(
                i != vi_tri and ban.mssv.casefold() == ma_moi
                for i, ban in enumerate(danh_sach)
            ):
                raise ValueError(f"MSSV {sinh_vien.mssv} đã tồn tại.")

            danh_sach[vi_tri] = sinh_vien
            ghi_du_lieu(danh_sach)
            return sinh_vien

    return None