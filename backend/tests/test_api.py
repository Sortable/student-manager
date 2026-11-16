import pytest
from fastapi.testclient import TestClient

import storage
from main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    tep_tam = tmp_path / "sinh_vien.json"
    monkeypatch.setattr(storage, "TEP_DU_LIEU", tep_tam)

    with TestClient(app) as client_kiem_thu:
        yield client_kiem_thu


@pytest.fixture
def sinh_vien_mau():
    return {
        "mssv": "TEST01",
        "ho_ten": "Sinh viên mẫu",
        "danh_sach_mon": [
            {"ten_mon": "Python", "diem_40": 8, "diem_60": 9},
        ],
    }


def test_them_va_doc_lai_sinh_vien(client, sinh_vien_mau):
    phan_hoi_them = client.post("/students", json=sinh_vien_mau)

    assert phan_hoi_them.status_code == 201
    assert phan_hoi_them.json()["gpa"] == pytest.approx(8.6)
    assert storage.TEP_DU_LIEU.is_file()

    phan_hoi_doc = client.get("/students")

    assert phan_hoi_doc.status_code == 200
    assert phan_hoi_doc.json() == [phan_hoi_them.json()]


@pytest.mark.parametrize("diem_sai", [-1, 11])
def test_tu_choi_diem_ngoai_khoang(client, sinh_vien_mau, diem_sai):
    sinh_vien_mau["danh_sach_mon"][0]["diem_40"] = diem_sai

    phan_hoi = client.post("/students", json=sinh_vien_mau)

    assert phan_hoi.status_code == 422
    assert not storage.TEP_DU_LIEU.exists()

def test_cap_nhat_mssv_va_tinh_lai_gpa(client, sinh_vien_mau):
    phan_hoi_them = client.post("/students", json=sinh_vien_mau)
    assert phan_hoi_them.status_code == 201

    sinh_vien_mau["mssv"] = "TEST02"
    sinh_vien_mau["danh_sach_mon"][0]["diem_40"] = 10

    phan_hoi_sua = client.put(
        "/students",
        params={"mssv_cu": "TEST01"},
        json=sinh_vien_mau,
    )

    assert phan_hoi_sua.status_code == 200
    assert phan_hoi_sua.json()["mssv"] == "TEST02"
    assert phan_hoi_sua.json()["gpa"] == pytest.approx(9.4)

    phan_hoi_doc = client.get("/students")
    assert phan_hoi_doc.status_code == 200
    assert phan_hoi_doc.json() == [phan_hoi_sua.json()]


def test_tu_choi_doi_sang_mssv_da_ton_tai(client, sinh_vien_mau):
    phan_hoi_them = client.post("/students", json=sinh_vien_mau)
    assert phan_hoi_them.status_code == 201

    sinh_vien_thu_hai = {**sinh_vien_mau, "mssv": "TEST02"}
    phan_hoi_them = client.post("/students", json=sinh_vien_thu_hai)
    assert phan_hoi_them.status_code == 201

    du_lieu_truoc_khi_sua = storage.TEP_DU_LIEU.read_bytes()
    phan_hoi_sua = client.put(
        "/students",
        params={"mssv_cu": "TEST01"},
        json={**sinh_vien_mau, "mssv": "test02"},
    )

    assert phan_hoi_sua.status_code == 409
    assert storage.TEP_DU_LIEU.read_bytes() == du_lieu_truoc_khi_sua