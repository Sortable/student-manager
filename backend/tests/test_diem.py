import pytest

from services import tinh_diem_mon, tinh_gpa


@pytest.mark.parametrize(
    "diem_40, diem_60, mong_doi",
    [
        (8, 9, 8.6),
        (8, 8.75, 8.5),
        (0, 0, 0.0),
        (10, 10, 10.0),
    ],
)
def test_tinh_diem_mon(diem_40, diem_60, mong_doi):
    assert tinh_diem_mon(diem_40, diem_60) == pytest.approx(mong_doi)


def test_tinh_gpa_hai_mon():
    assert tinh_gpa([8.6, 7.7]) == pytest.approx(8.15)