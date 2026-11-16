import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from fastapi import HTTPException

import main
import storage
from schemas import SinhVienDauVao


class TestLoiGhiSinhVien(unittest.TestCase):
    def test_tao_sinh_vien_tra_500_khi_ghi_loi(self):
        sinh_vien_mau = SinhVienDauVao(
            mssv="TEST01",
            ho_ten="Sinh viên mẫu",
            danh_sach_mon=[
                {"ten_mon": "Python", "diem_40": 8, "diem_60": 9},
            ],
        )

        with TemporaryDirectory() as thu_muc:
            tep_json = Path(thu_muc) / "sinh_vien.json"
            tep_json.write_text("[]", encoding="utf-8")
            noi_dung_truoc = tep_json.read_bytes()

            with patch.object(storage, "TEP_DU_LIEU", tep_json):
                with patch(
                    "main.them_sinh_vien",
                    side_effect=RuntimeError("Lỗi ghi giả lập"),
                ) as ghi:
                    with self.assertRaises(HTTPException) as loi:
                        main.tao_sinh_vien(sinh_vien_mau)

                    self.assertEqual(loi.exception.status_code, 500)
                    ghi.assert_called_once()

            self.assertEqual(tep_json.read_bytes(), noi_dung_truoc)