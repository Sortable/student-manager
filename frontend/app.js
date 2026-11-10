const bo_loc = document.getElementById("bo-loc");
const o_tim_kiem = document.getElementById("tu-khoa");
const chon_thu_tu = document.getElementById("thu-tu");
const nut_tim_kiem = document.getElementById("nut-tim-kiem");

let dang_tai = false;
let can_tai_lai = false;

const nut_tai_lai = document.getElementById("nut-tai-lai");

const thong_bao = document.getElementById("thong-bao");

const bang_sinh_vien = document.getElementById(
    "danh-sach-sinh-vien"
);


function them_o(dong, gia_tri) {
    const o = document.createElement("td");

    o.textContent = String(gia_tri);
    dong.appendChild(o);

    return o;
}


function hien_thi_danh_sach(danh_sach_sinh_vien) {
    bang_sinh_vien.replaceChildren();

    for (const sinh_vien of danh_sach_sinh_vien) {
        const dong = document.createElement("tr");

        them_o(dong, sinh_vien.mssv);
        them_o(dong, sinh_vien.ho_ten);
        them_o(dong, sinh_vien.danh_sach_mon.length);

        const o_gpa = them_o(
            dong,
            sinh_vien.gpa.toFixed(2)
        );

        o_gpa.classList.add("cot-diem", "diem-noi-bat");

        const o_thao_tac = document.createElement("td");
        o_thao_tac.classList.add("cot-thao-tac");

        const nut_chi_tiet = document.createElement("button");

        nut_chi_tiet.type = "button";
        nut_chi_tiet.textContent = "Xem chi tiết";

        nut_chi_tiet.classList.add(
            "nut-phu",
            "nut-chi-tiet"
        );

        nut_chi_tiet.setAttribute(
            "aria-label",
            `Xem chi tiết sinh viên ${sinh_vien.mssv}`
        );

        nut_chi_tiet.addEventListener("click", function () {
            mo_chi_tiet_sinh_vien(sinh_vien);
        });

        const nut_chinh_sua = document.createElement("button");
        nut_chinh_sua.type = "button";
        nut_chinh_sua.textContent = "Chỉnh sửa";
        nut_chinh_sua.classList.add("nut-phu", "nut-chi-tiet");
        nut_chinh_sua.setAttribute(
            "aria-label",
            `Chỉnh sửa sinh viên ${sinh_vien.mssv}`
        );
        nut_chinh_sua.addEventListener("click", function () {
            mo_bieu_mau_chinh_sua(sinh_vien);
        });

        o_thao_tac.append(nut_chi_tiet, " ", nut_chinh_sua);
        dong.appendChild(o_thao_tac);

        bang_sinh_vien.appendChild(dong);
    }
}

function dinh_dang_gpa(gia_tri) {
    if (gia_tri === null) {
        return "—";
    }

    return gia_tri.toFixed(2);
}


function dinh_dang_sinh_vien(danh_sach_sinh_vien) {
    if (danh_sach_sinh_vien.length === 0) {
        return "—";
    }

    const danh_sach_ten = [];

    for (const sinh_vien of danh_sach_sinh_vien) {
        danh_sach_ten.push(
            `${sinh_vien.mssv} — ${sinh_vien.ho_ten}`
        );
    }

    return danh_sach_ten.join("; ");
}


async function tai_thong_ke() {
    const thong_bao_thong_ke = document.getElementById(
        "thong-bao-thong-ke"
    );

    const cac_o_thong_ke = [
        "tong-sinh-vien",
        "gpa-cao-nhat",
        "gpa-thap-nhat",
        "gpa-trung-binh",
        "sinh-vien-cao-nhat",
        "sinh-vien-thap-nhat",
    ];

    for (const ma_phan_tu of cac_o_thong_ke) {
        document.getElementById(ma_phan_tu).textContent = "—";
    }

    thong_bao_thong_ke.textContent = "Đang tải thống kê...";
    thong_bao_thong_ke.classList.remove("loi");

    try {
        const phan_hoi = await fetch("/students/statistics");

        if (!phan_hoi.ok) {
            throw new Error(
                `Yêu cầu thống kê thất bại: ${phan_hoi.status}`
            );
        }

        const du_lieu = await phan_hoi.json();

        document.getElementById("tong-sinh-vien").textContent =
            du_lieu.so_luong_sinh_vien;

        document.getElementById("gpa-cao-nhat").textContent =
            dinh_dang_gpa(du_lieu.gpa_cao_nhat);

        document.getElementById("gpa-thap-nhat").textContent =
            dinh_dang_gpa(du_lieu.gpa_thap_nhat);

        document.getElementById("gpa-trung-binh").textContent =
            dinh_dang_gpa(du_lieu.gpa_trung_binh);

        document.getElementById("sinh-vien-cao-nhat").textContent =
            dinh_dang_sinh_vien(du_lieu.sinh_vien_cao_nhat);

        document.getElementById("sinh-vien-thap-nhat").textContent =
            dinh_dang_sinh_vien(du_lieu.sinh_vien_thap_nhat);

        thong_bao_thong_ke.textContent = "";
    } catch (loi) {
        thong_bao_thong_ke.textContent =
            "Không tải được thống kê. Vui lòng thử tải lại dữ liệu.";

        thong_bao_thong_ke.classList.add("loi");

        console.error(loi);
    }
}


async function tai_danh_sach_sinh_vien() {
    if (dang_tai) {
    can_tai_lai = true;
    return;
}

    dang_tai = true;

    const tu_khoa = o_tim_kiem.value.trim();

    const cac_dieu_khien = [
        nut_tai_lai,
        nut_tim_kiem,
        o_tim_kiem,
        chon_thu_tu,
    ];

    for (const phan_tu of cac_dieu_khien) {
        phan_tu.disabled = true;
    }

    thong_bao.textContent = "Đang tải dữ liệu...";
    thong_bao.classList.remove("loi");

    try {
    await tai_thong_ke();

    const tham_so = new URLSearchParams();

        tham_so.set("thu_tu", chon_thu_tu.value);

        if (tu_khoa !== "") {
            tham_so.set("tu_khoa", tu_khoa);
        }

        const phan_hoi = await fetch(
            `/students?${tham_so.toString()}`
        );

        if (!phan_hoi.ok) {
            throw new Error(
                `Yêu cầu thất bại với mã ${phan_hoi.status}`
            );
        }

        const danh_sach_sinh_vien = await phan_hoi.json();

        hien_thi_danh_sach(danh_sach_sinh_vien);

        if (danh_sach_sinh_vien.length === 0) {
            thong_bao.textContent =
                "Không tìm thấy sinh viên phù hợp.";
        } else {
            thong_bao.textContent =
                `Hiển thị ${danh_sach_sinh_vien.length} sinh viên.`;
        }
    } catch (loi) {
        bang_sinh_vien.replaceChildren();

        thong_bao.textContent =
            "Không tải được danh sách. Vui lòng thử lại.";

        thong_bao.classList.add("loi");

        console.error(loi);
    } finally {
        for (const phan_tu of cac_dieu_khien) {
            phan_tu.disabled = false;
        }

        dang_tai = false;
        
        if (can_tai_lai) {
            can_tai_lai = false;
            tai_danh_sach_sinh_vien();
        }
    }
}


nut_tai_lai.addEventListener(
    "click",
    tai_danh_sach_sinh_vien
);

bo_loc.addEventListener("submit", function (su_kien) {
    su_kien.preventDefault();

    tai_danh_sach_sinh_vien();
});

chon_thu_tu.addEventListener(
    "change",
    tai_danh_sach_sinh_vien
);

tai_danh_sach_sinh_vien();