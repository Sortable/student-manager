const hop_thoai_chi_tiet = document.getElementById(
    "hop-thoai-chi-tiet"
);

const thong_tin_chi_tiet = document.getElementById(
    "thong-tin-chi-tiet"
);

const gpa_chi_tiet = document.getElementById(
    "gpa-chi-tiet"
);

const bang_mon_chi_tiet = document.getElementById(
    "mon-hoc-chi-tiet"
);


function mo_chi_tiet_sinh_vien(sinh_vien) {
    thong_tin_chi_tiet.textContent =
        `${sinh_vien.mssv} — ${sinh_vien.ho_ten}`;

    gpa_chi_tiet.textContent = sinh_vien.gpa.toFixed(2);

    bang_mon_chi_tiet.replaceChildren();

    for (const mon of sinh_vien.danh_sach_mon) {
        const dong = document.createElement("tr");

        them_o(dong, mon.ten_mon);

        const o_diem_40 = them_o(dong, mon.diem_40);
        o_diem_40.classList.add("cot-diem");

        const o_diem_60 = them_o(dong, mon.diem_60);
        o_diem_60.classList.add("cot-diem");

        const o_tong_ket = them_o(
            dong,
            mon.diem_tong_ket.toFixed(1)
        );

        o_tong_ket.classList.add(
            "cot-diem",
            "diem-noi-bat"
        );

        bang_mon_chi_tiet.appendChild(dong);
    }

    if (!hop_thoai_chi_tiet.open) {
        hop_thoai_chi_tiet.showModal();
    }
}